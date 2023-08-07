'''
起始时随机买入N支股票，每天卖掉收益最差的M支，再随机买入剩余股票池的M支
改进：买入历史收益率最低的N支股票，调仓日留下反转程度大的股票，卖掉表现
最差的M支，再买入收益率最低的M支
随机选股，周期调仓




'''
from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    log.info('START')
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    g.security = get_index_stocks('000300.XSHG') # A股也行000002
    g.period = 30
    g.N = 10 # 一共买多少支
    g.change = 1 # 每次调整多少支
    g.init = True # 
    run_monthly(handle, 1)

def get_sorted_stocks(context, stocks):
    df = history(g.period, field='close', security_list=stocks).T
    df['ret'] = (df.iloc[:,len(df.columns)-1]-df.iloc[:,0]) / df.iloc[:,0]
    df = df.sort_values(by='ret', ascending=True)
    return df.index.values
    
def handle(context):
    # 只在初始的时候执行买入N支
    if g.init:
        # 排序，选择前N支
        stocks = get_sorted_stocks(context, g.security)[:g.N]
        cash = context.portfolio.available_cash * 0.9 / len(stocks)
        for stock in stocks:
            order_value(stock, cash)
        g.init = False
        return
    
    # 后续调仓
    # 选出现在仓内最差的M支卖出
    stocks = get_sorted_stocks(context, list(context.portfolio.positions.keys))
    for stock in stocks[-g.change:]:
        order_target(stock, 0)
        
    # 在所有股票中选最差的M支买入
    stocks = get_sorted_stocks(context, g.security)
    
    for stock in stocks:
        if len(context.portfolio.positions) >= g.N:
            break
        if stock not in context.portfolio.positions:
            order_value(stock, context.portfolio.available_cash * 0.9)
   
