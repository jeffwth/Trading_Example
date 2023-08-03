# 因子：选择股票的某种标准，增长率、市值、市盈率、净资产收益率等
# 对于某个因子，选取表现最好(因子最大或最小)的N支股票持仓，每隔一段时间调仓一次

# 小市值策略：找到市值最小的N支进行持仓
from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    log.info('START')
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    
    # 看沪深300，从valuation表中选取code和market_cap
    g.security = get_index_stocks('000300.XSHG')
    g.q = query(valuation).filter(valuation.code.in_(g.security))
    g.N = 10
    # 每个月的第一个交易日执行func
    run_monthly(func, 1)
    
def func(context):
    df = get_fundamentals(g.q)[['code', 'market_cap']]
    df = df.sort_values('market_cap').iloc[:g.N,:]
    
    # 需要买的股票
    to_hold = df['code'].values
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
    
    
    
    
    
    
    
    
