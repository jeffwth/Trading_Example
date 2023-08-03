# 多因子选股
# 把需要考虑的因子进行标准化加权打分
# 市值小和净资产收益率高
from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    log.info('START')
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    
    # 看沪深300，从valuation表中选取code和market_cap
    g.security = get_index_stocks('000300.XSHG')
    g.q = query(valuation, indicator).filter(valuation.code.in_(g.security))
    g.N = 10
    # 每个月的第一个交易日执行func
    run_monthly(func, 1)
    
def func(context):
    # 选取股票代码，市值和ROE
    df = get_fundamentals(g.q)[['code', 'market_cap', 'roe']]
    # 市值,ROE标准化
    df['market_cap'] = (df['market_cap'] - df['market_cap'].min()) / (df['market_cap'].max() - df['market_cap'].min())
    df['roe'] = (df['roe'] - df['roe'].min()) / (df['roe'].max() - df['roe'].min())
    # 算得分
    df['score'] = df['roe'] - df['market_cap']
    
    # 排序选股票
    df = df.sort_values('score').iloc[-g.N:,:]
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
    
    
    
    
    
    
    
    