import re


def get_eating_account(from_user, description, time=None):
    if time == None or not hasattr(time, 'hour'):
        return 'Expenses:Eating:Others'
    elif time.hour <= 3 or time.hour >= 21:
        return 'Expenses:Eating:Nightingale'
    elif time.hour <= 10:
        return 'Expenses:Eating:Breakfast'
    elif time.hour <= 16:
        return 'Expenses:Eating:Lunch'
    else:
        return 'Expenses:Eating:Supper'


def get_credit_return(from_user, description, time=None):
    for key, value in credit_cards.items():
        if key == from_user:
            return value
    return "Unknown"


public_accounts = [
    'Assets:Company:Alipay:StupidAlipay'
]

credit_cards = {
    '中信银行': 'Liabilities:CreditCard:CITIC',
}

accounts = {
    "余额宝": 'Assets:AliPay:MonetaryFund',
    "单车骑行卡抵扣": 'Assets:Hello:Card',
    "(账户)?余额": 'Assets:AliPay:Balance',
    '花呗': 'Liabilities:AliPay:AntCreditPay',
    '招商银行储蓄卡': 'Assets:DebitCard:ChinaMerchantsBank:0387',
    '招商银行信用卡': 'Liabilities:CreditCard:ChinaMerchantsBank',
    '中国银行储蓄卡': 'Assets:DebitCard:BankOfChina:9704',
    '中国银行信用卡': 'Liabilities:CreditCard:BankOfChina:6649',
    '平安银行信用卡': 'Liabilities:CreditCard:PingAnBank:8143',
    '广发银行信用卡': 'Liabilities:CreditCard:ChinaGuangfaBank',
    '交通银行信用卡': 'Liabilities:CreditCard:BankOfCommunications',
    '工商银行储蓄卡': 'Assets:DebitCard:IndustrialAndCommercialBankOfChina',
    '网商银行储蓄卡': 'Assets:DebitCard:MyBank',
    '农业银行储蓄卡': 'Assets:DebitCard:AgriculturalBankOfChina',
    '赣州银行储蓄卡': 'Assets:DebitCard:GanZhouBank',
    '红包': 'Assets:Unknown',
}

descriptions = {
    '余额宝.*收益发放': 'Assets:AliPay:MonetaryFund',
    '.*花呗.*还款.*账单': 'Liabilities:AliPay:AntCreditPay',
    '好医保': 'Expenses:Others:Service:Insure',
    '牙刷': 'Expenses:Life:PersonalCare',
    '(中国石油|加油|充电订单免密支付|特来电)': 'Expenses:Transport:Traffic:Fuel',
    '(平安财产保险|租车|(高速)?通行费)': 'Expenses:Transport:Traffic:Usage',
    '(迪卡侬|服饰|(休闲|运动)裤|马登(工装)?)': 'Expenses:Dress:Clothing',
    '(公交|火车票|滴滴快车|高德.*打车|T3出行|地铁|哈啰单车骑行|骑行卡|哈啰打车)': 'Expenses:Transport:Traffic:Fee',
    '智能货柜消费': 'Expenses:Food:Beverage',
    '(中国邮政|寄件费|运费|货拉拉费用)': 'Expenses:Transport:Communicate:PostalService',
    '(阿里云|(话费|流量).*充值|中国(电信|联通))': 'Expenses:Transport:Communicate:Telecom',
    '酒店': 'Expenses:Others:Service:Hotel',
    '(美食|朴朴|华(南理)?工.*饭堂)': 'Expenses:Food:Serve',
    '书籍': 'Expenses:CultureRecreation:Stuff',
    '水费': 'Expenses:Housing:Consume:Water',
    '(理疗|校医室|人民医院)': 'Expenses:Health:Service:Visit',
    '(剪映.*(订阅|服务)|省钱卡)': 'Expenses:CultureRecreation:Service',
    '物业管理': 'Expenses:Housing:Maintenance:Property',
    '(学贷还款|考试费)': 'Expenses:Education:High',
    '美发': 'Expenses:Others:Service:Hairdressing',
}

anothers = {
    '上海拉扎斯': get_eating_account
}

incomes = {
    '余额宝.*收益发放': 'Income:Trade:PnL',
    '(抖音极速版|淘宝天天得现金活动)提现': 'Income:RedEnvelope',
}

description_res = dict([(key, re.compile(key)) for key in descriptions])
another_res = dict([(key, re.compile(key)) for key in anothers])
income_res = dict([(key, re.compile(key)) for key in incomes])
account_res = dict([(key, re.compile(key)) for key in accounts])
