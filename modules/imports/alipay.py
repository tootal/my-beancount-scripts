import re
from zipfile import ZipFile
from datetime import date
from io import StringIO, BytesIO

import dateparser
from beancount.core import data
from beancount.core.data import Note, Transaction

from . import (DictReaderStrip, get_account_by_guess,
               get_income_account_by_guess,
               get_pay_account_by_pay_channel)
from .base import Base
from .deduplicate import Deduplicate

AccountHuaBei = 'Liabilities:AliPay:AntCreditPay'
AccountYuEBao = 'Assets:AliPay:MonetaryFund'

class Alipay(Base):

    def __init__(self, filename, byte_content, entries, option_map):
        if re.search(r'alipay_record_.*\.zip$', filename):
            z = ZipFile(BytesIO(byte_content), 'r')
            filelist = z.namelist()
            if len(filelist) == 1 and re.search(r'alipay_record.*\.csv$', filelist[0]):
                byte_content = z.read(filelist[0])
        content = byte_content.decode('gbk')
        lines = content.split("\n")
        start_index = 0
        start_line = '------------------------支付宝（中国）网络技术有限公司  电子客户回单------------------------'
        for index in range(len(lines)):
            if str(lines[index]).strip() == start_line:
                start_index = index
                break
        if str(lines[start_index]).strip() != start_line:
            raise RuntimeError('Not Alipay Trade Record!')
        content = "\n".join(lines[start_index+1:])
        self.content = content
        self.deduplicate = Deduplicate(entries, option_map)

    def parse(self):
        content = self.content
        f = StringIO(content)
        reader = DictReaderStrip(f, delimiter=',')
        transactions = []
        for row in reader:
            if row['交易状态'] == '交易关闭':
                continue
            if row['交易状态'] == '冻结成功':
                continue
            time = None
            if '付款时间' in row:
                time = row['付款时间']
            elif '交易创建时间' in row:
                time = row['交易创建时间']
            elif '交易时间' in row:
                time = row['交易时间']
            name = None
            if '商品名称' in row:
                name = row['商品名称']
            elif '商品说明' in row:
                name = row['商品说明']
            alipay_trade_no = None
            if '交易号' in row:
                alipay_trade_no = row['交易号']
            elif '交易订单号' in row:
                alipay_trade_no = row['交易订单号']
            amount = None
            if '金额（元）' in row:
                amount = float(row['金额（元）'])
            elif '金额' in row:
                amount = float(row['金额'])
            print("Importing {} at {}".format(name, time))
            money_status = None
            if '资金状态' in row:
                money_status = row['资金状态']
            elif '收/支' in row:
                money_status = row['收/支']
            meta = {}
            time = dateparser.parse(time)
            meta['alipay_trade_no'] = alipay_trade_no
            meta['trade_time'] = str(time)
            meta['timestamp'] = str(time.timestamp()).replace('.0', '')
            if '交易分类' in row:
                meta['trade_class'] = row['交易分类']
            if '收/付款方式' in row:
                meta['pay_channel'] = row['收/付款方式']
            if '对方账号' in row and row['对方账号'] != '/':
                meta['payee_account'] = row['对方账号']
            expenses_account = get_account_by_guess(row['交易对方'], name, time, meta['trade_class'])
            pay_account = get_pay_account_by_pay_channel(meta['pay_channel'])
            flag = "*"
            if expenses_account == "Expenses:Unknown":
                flag = "!"
            if pay_account == 'Assets:Unknown':
                flag = '!'
            if row['备注'] != '':
                meta['note'] = row['备注']

            if row['商家订单号'] != '':
                meta['shop_trade_no'] = row['商家订单号']

            meta = data.new_metadata(
                'beancount/moneybook.beancount',
                12345,
                meta
            )
            entry = Transaction(
                meta,
                date(time.year, time.month, time.day),
                flag,
                row['交易对方'],
                name,
                data.EMPTY_SET,
                data.EMPTY_SET, []
            )
            price = amount
            if money_status in ['支出', '已支出']:
                data.create_simple_posting(entry, pay_account, -price, 'CNY')
            elif money_status == '资金转移':
                data.create_simple_posting(entry, pay_account, price, 'CNY')
            elif money_status == '不计收支':
                if name.startswith('退款'):
                    data.create_simple_posting(entry, pay_account, price, 'CNY')
                    price = -price
                elif name.startswith('花呗主动还款'):
                    price = -price
                    data.create_simple_posting(entry, pay_account, price, 'CNY')
                elif re.findall('余额宝.*收益发放', name):
                    data.create_simple_posting(entry, 'Income:PassiveIncome:MoneyFund', -price, 'CNY')
                elif re.findall('(余额宝.*更换货基转入|支付宝转入到余利宝|余额宝-自动转入|蚂蚁财富.*买入|转账收款到余额宝)', name):
                    continue
                else:
                    raise RuntimeError('Unknown money status')
            elif money_status in ['收入', '已收入']:
                if row['交易状态'] == '退款成功':
                    # 收钱码收款时，退款成功时资金状态为已支出
                    price = -price
                    data.create_simple_posting(entry, pay_account, price, 'CNY')
                else:
                    income = get_income_account_by_guess(
                        row['交易对方'], name, time)
                    if income == 'Income:Unknown':
                        entry = entry._replace(flag='!')
                    data.create_simple_posting(entry, income, -price, 'CNY')
            else:
                print('Unknown status')
                print(row)
                raise RuntimeError('Unknown money status')

            data.create_simple_posting(entry, expenses_account, price, 'CNY')
            if '服务费（元）' in row and row['服务费（元）'] != '0.00':
                data.create_simple_posting(
                    entry, 'Expenses:Finance:Fee', row['服务费（元）'], 'CNY')

            #b = printer.format_entry(entry)
            # print(b)
            if not self.deduplicate.find_duplicate(entry, amount, 'alipay_trade_no'):
                transactions.append(entry)

        self.deduplicate.apply_beans()
        return transactions
