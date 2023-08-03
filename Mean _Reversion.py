# 跌下去的迟早会涨上来
# 价格的波动一般会以它的均线为中心。当标的价格由于波动而偏离移动均线时，
# 它将调整并重新归于均线
# 偏离程度：(MA-P)/MA

'''
策略：
在每个调仓日进行
计算池内所有股票的N日均线
计算池内所有股票和均线的偏离度
选取偏离度最高的M支股票并调仓
'''

from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    log.info('START')
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    
    g.security = get_index_stocks('000300.XSHG')
    g.ma_days = 30 # 30日均线
    g.stock_num = 10 #持仓10支gu
    run_monthly(func, 1)

def func(context):
    # sr中储存股票代码和偏离程度
    sr = pd.Series(index=g.security)
    for stock in sr.index:
        # 计算30日均线
        ma = attribute_history(stock, g.ma_days)['close'].mean()
        # 计算当前价格
        p = get_current_data()[stock].day_open
        # 计算偏离程度
        ratio = (ma - p) / ma
        sr[stock] = ratio
    # 找到最大的M个
    to_hold = sr.nlargest(g.stock_num).index.values
    
    # 如果现在持有的股票不在需要购买的名单上，就全部售出
    for stock in context.portfolio.positions:
        if stock not in to_hold:
            order_target(stock, 0)
    
    # 要买的股票 如果要买的股票不在现有的仓中，买入
    to_buy = [stock for stock in to_hold if stock not in context.portfolio.positions]
    
    if len(to_buy) > 0: # 排除要买的和持有的股票全部一样的情况，有变动才会调仓
        cash_per_stock = context.portfolio.available_cash / len(to_buy)
        for stock in to_buy:
            order_value(stock, cash_per_stock) # 把可用的钱平均分配给每一支需要买的股票
    
    
    
