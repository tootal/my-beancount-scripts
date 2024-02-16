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
    "(账户)?余额": 'Assets:AliPay:Balance',
    '花呗': 'Liabilities:AliPay:AntCreditPay',
    '招商银行储蓄卡': 'Assets:DebitCard:ChinaMerchantsBank',
    '招商银行信用卡': 'Liabilities:CreditCard:ChinaMerchantsBank',
    '中国银行储蓄卡': 'Assets:DebitCard:BankOfChina:9704',
    '中国银行信用卡': 'Liabilities:CreditCard:BankOfChina',
    '平安银行信用卡': 'Liabilities:CreditCard:PingAnBank',
    '广发银行信用卡': 'Liabilities:CreditCard:ChinaGuangfaBank',
    '交通银行信用卡': 'Liabilities:CreditCard:BankOfCommunications',
    '工商银行储蓄卡': 'Assets:DebitCard:IndustrialAndCommercialBankOfChina',
}

descriptions = {
    '高德.*打车': 'Expenses:Transport:Traffic:Fee',
    '余额宝.*收益发放': 'Assets:AliPay:MonetaryFund',
    '.*花呗.*还款.*账单': 'Liabilities:AliPay:AntCreditPay',
    '好医保': 'Expenses:Others:Service:Insure',
    '牙刷': 'Expenses:Life:PersonalCare',
    '(加油|充电订单免密支付|特来电)': 'Expenses:Transport:Traffic:Fuel',
    '(高速)?通行费': 'Expenses:Transport:Traffic:Usage',
    '(服饰|(休闲|运动)裤|马登(工装)?)': 'Expenses:Dress:Clothing',
    '(地铁|骑行卡)': 'Expenses:Transport:Traffic:Fee',
    '智能货柜消费': 'Expenses:Food:Beverage',
    '(寄件费|运费)': 'Expenses:Transport:Communicate:PostalService',
    '(阿里云|话费充值)': 'Expenses:Transport:Communicate:Telecom',
    '酒店': 'Expenses:Others:Service:Hotel',
    '(美食|朴朴)': 'Expenses:Food:Serve',
    '书籍': 'Expenses:CultureRecreation:Stuff',
    '水费': 'Expenses:Housing:Consume:Water',
    '理疗': 'Expenses:Health:Service:Visit',
}

anothers = {
    '上海拉扎斯': get_eating_account
}

incomes = {
    '余额宝.*收益发放': 'Income:Trade:PnL',
}

description_res = dict([(key, re.compile(key)) for key in descriptions])
another_res = dict([(key, re.compile(key)) for key in anothers])
income_res = dict([(key, re.compile(key)) for key in incomes])
account_res = dict([(key, re.compile(key)) for key in accounts])
