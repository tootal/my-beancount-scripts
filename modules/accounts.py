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
    '招商银行储蓄卡': 'Assets:DebitCard:CMB:0387',
    '招商银行(0387)': 'Assets:DebitCard:CMB:0387',
    '招商银行信用卡': 'Liabilities:CreditCard:CMB:2445',
    '招商银行(2445)': 'Liabilities:CreditCard:CMB:2445',
    '中国银行储蓄卡': 'Assets:DebitCard:BOC:9704',
    '中国银行(9704)': 'Assets:DebitCard:BOC:9704',
    '中国银行信用卡': 'Liabilities:CreditCard:BOC:6649',
    '中国银行(6649)': 'Liabilities:CreditCard:BOC:6649',
    '平安银行信用卡': 'Liabilities:CreditCard:PAB:8143',
    '平安银行(8143)': 'Liabilities:CreditCard:PAB:8143',
    '广发银行信用卡': 'Liabilities:CreditCard:GDB:4422',
    '广发银行(4422)': 'Liabilities:CreditCard:GDB:4422',
    '交通银行信用卡': 'Liabilities:CreditCard:BCM:4862',
    '交通银行(4865)': 'Liabilities:CreditCard:BCM:4862',
    '工商银行储蓄卡': 'Assets:DebitCard:ICBC:3990',
    '工商银行(3990)': 'Assets:DebitCard:ICBC:3990',
    '网商银行储蓄卡': 'Assets:DebitCard:MyBank',
    '农业银行': 'Assets:DebitCard:ABC:7276',
    '农业银行储蓄卡': 'Assets:DebitCard:ABC:7276',
    '农业银行(7276)': 'Assets:DebitCard:ABC:7276',
    '赣州银行储蓄卡': 'Assets:DebitCard:GanZhouBank',
    '赣州银行(3351)': 'Assets:DebitCard:GanZhouBank',
    '微众银行(7378)': 'Assets:DebitCard:WeBank',
    '广州银行(2473)': 'Liabilities:CreditCard:GCB:2473',
    '红包': 'Assets:Unknown',
    '零钱': 'Assets:WeChat:Pocket',
    '零钱通': 'Assets:WeChat:Lingqiantong',
}

descriptions = {
    '余额宝.*收益发放': 'Assets:AliPay:MonetaryFund',
    '.*花呗.*还款.*账单': 'Liabilities:AliPay:AntCreditPay',
    '好医保': 'Expenses:Others:Service:Insure',
    '牙刷': 'Expenses:Life:PersonalCare',
    '(中国石油|加油|充电订单免密支付|劲桩|特来电|壳牌充电|延长壳牌广东)': 'Expenses:Transport:Traffic:Fuel',
    '(平安财产保险|租车|(高速)?通行费|停车场|停车费)': 'Expenses:Transport:Traffic:Usage',
    '(迪卡侬|服饰|(休闲|运动)裤|马登(工装)?)': 'Expenses:Dress:Clothing',
    '(公交|火车票|滴滴快车|高德.*打车|T3出行|地铁|哈啰单车骑行|骑行卡|哈啰打车|岭南通|羊城通)': 'Expenses:Transport:Traffic:Fee',
    '智能货柜消费': 'Expenses:Food:Beverage',
    '(中国邮政|寄件费|运费|货拉拉费用|悟空100)': 'Expenses:Transport:Communicate:PostalService',
    '(阿里云|(话费|流量).*充值|中国(电信|联通))': 'Expenses:Transport:Communicate:Telecom',
    '酒店': 'Expenses:Others:Service:Hotel',
    '(美食|餐厅|烤肉店|朴朴|华(南理)?工.*饭堂|炒栗子|意面)': 'Expenses:Food:Serve',
    '书籍|鲜花|景区门票': 'Expenses:CultureRecreation:Stuff',
    '(水费|天天一泉售水机)': 'Expenses:Housing:Consume:Water',
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
