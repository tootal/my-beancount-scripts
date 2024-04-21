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
    "余额宝": 'Assets:01-流动资金:04-互联网金融:04-支付宝余额宝',
    "单车骑行卡抵扣": 'Assets:05-其他:01-哈啰骑行卡',
    "(账户)?余额": 'Assets:01-流动资金:04-互联网金融:02-支付宝余额',
    '花呗': 'Liabilities:02-互联网金融:01-支付宝花呗',
    '招商银行储蓄卡': 'Assets:01-流动资金:03-借记卡:CMB-招商银行-0387',
    '招商银行(0387)': 'Assets:01-流动资金:03-借记卡:CMB-招商银行-0387',
    '招商银行信用卡': 'Liabilities:01-信用卡:CMB-招商银行-2445',
    '招商银行(2445)': 'Liabilities:01-信用卡:CMB-招商银行-2445',
    '中国银行储蓄卡': 'Assets:01-流动资金:03-借记卡:BOC-中国银行-9704',
    '中国银行(9704)': 'Assets:01-流动资金:03-借记卡:BOC-中国银行-9704',
    '中国银行信用卡': 'Liabilities:01-信用卡:BOC-中国银行-6649',
    '中国银行(6649)': 'Liabilities:01-信用卡:BOC-中国银行-6649',
    '平安银行信用卡': 'Liabilities:01-信用卡:PAB-平安银行-8143',
    '平安银行(8143)': 'Liabilities:01-信用卡:PAB-平安银行-8143',
    '广发银行信用卡': 'Liabilities:01-信用卡:GDB-广发银行-4422',
    '广发银行(4422)': 'Liabilities:01-信用卡:GDB-广发银行-4422',
    '交通银行信用卡': 'Liabilities:01-信用卡:BCM-交通银行-4862',
    '交通银行(4865)': 'Liabilities:01-信用卡:BCM-交通银行-4862',
    '工商银行储蓄卡': 'Assets:01-流动资金:03-借记卡:ICBC-工商银行-3990',
    '工商银行(3990)': 'Assets:01-流动资金:03-借记卡:ICBC-工商银行-3990',
    '网商银行储蓄卡': 'Assets:01-流动资金:03-借记卡:MyBank-网商银行-1634',
    '农业银行': 'Assets:01-流动资金:03-借记卡:ABC-农业银行-7276',
    '农业银行储蓄卡': 'Assets:01-流动资金:03-借记卡:ABC-农业银行-7276',
    '农业银行(7276)': 'Assets:01-流动资金:03-借记卡:ABC-农业银行-7276',
    '赣州银行储蓄卡': 'Assets:01-流动资金:03-借记卡:GZB-赣州银行-3351',
    '赣州银行(3351)': 'Assets:01-流动资金:03-借记卡:GZB-赣州银行-3351',
    '微众银行(7378)': 'Assets:DebitCard:WeBank',
    '广州银行(2473)': 'Liabilities:01-信用卡:GCB-广州银行-2473',
    '红包': 'Assets:06-未知',
    '零钱': 'Assets:01-流动资金:04-互联网金融:01-微信零钱',
    '零钱通': 'Assets:WeChat:Lingqiantong',
}

descriptions = {
    '余额宝.*收益发放': 'Assets:01-流动资金:04-互联网金融:04-支付宝余额宝',
    '.*花呗.*还款.*账单': 'Liabilities:02-互联网金融:01-支付宝花呗',
    '好医保': 'Expenses:09-保险:01-医疗',
    '牙刷': 'Expenses:04-生活',
    '(中国石油|加油)': 'Expenses:05-交通:02-加油',
    '(充电订单免密支付|劲桩|特来电|壳牌充电|延长壳牌广东)': 'Expenses:05-交通:03-充电',
    '(停车场|停车费)': 'Expenses:05-交通:04-停车',
    '(平安财产保险)': 'Expenses:05-交通:05-保险',
    '((高速)?通行费)': 'Expenses:05-交通:06-过路',
    '(平安财产保险|租车|(高速)?通行费)': 'Expenses:Transport:Traffic:Usage',
    '(迪卡侬|服饰|(休闲|运动)裤|马登(工装)?)': 'Expenses:02-服饰',
    '(公交|火车票|滴滴快车|高德.*打车|T3出行|地铁|哈啰单车骑行|骑行卡|哈啰打车|岭南通|羊城通)': 'Expenses:05-交通:08-公交',
    '智能货柜消费': 'Expenses:01-饮食:02-饮品',
    '(中国邮政|寄件费|运费|货拉拉费用|悟空100)': 'Expenses:11-通信:02-邮递',
    '(阿里云|(话费|流量).*充值|中国(电信|联通))': 'Expenses:11-通信:01-电信',
    '酒店': 'Expenses:03-居住:04-酒店',
    '(美食|餐厅|烤肉店|朴朴|华(南理)?工.*饭堂|炒栗子|意面)': 'Expenses:01-饮食:03-餐饮服务',
    '书籍|鲜花|景区门票': 'Expenses:06-文化娱乐:03-用品',
    '(水费|天天一泉售水机)': 'Expenses:03-居住:03-水电',
    '(理疗|校医室|人民医院)': 'Expenses:07-医疗:01-服务',
    '(剪映.*(订阅|服务)|省钱卡)': 'Expenses:06-文化娱乐:04-服务',
    '物业管理': 'Expenses:03-居住:02-物业',
    '(学贷还款|考试费)': 'Expenses:06-文化娱乐:01-教育',
    '美发': 'Expenses:04-生活',
}

anothers = {
    '上海拉扎斯': get_eating_account
}

incomes = {
    '余额宝.*收益发放': 'Income:Trade:PnL',
    '(抖音极速版|淘宝天天得现金活动)提现': 'Income:04-红包',
}

description_res = dict([(key, re.compile(key)) for key in descriptions])
another_res = dict([(key, re.compile(key)) for key in anothers])
income_res = dict([(key, re.compile(key)) for key in incomes])
account_res = dict([(key, re.compile(key)) for key in accounts])
