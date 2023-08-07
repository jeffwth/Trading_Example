'''
彼得·林奇：任何一家公司股票如果定价合理的话，市盈率就会和收益增长率相等
市盈率(PE) = 股价(P) / 每股收益(EPS)
市盈率大约是市值/净收益

每股收益(EPS)
股价(P)
市盈率(PE)
收益增长率(G)

PE = P / EPS
G = (EPS[i] - EPS[i-1]) / EPS[i-1]
PEG = PE / (100 * G)
理想情况下PE = G, 即PEG = 0.01
PEG越低，代表股价被低估的可能性越大，股价会涨的可能性越大
PEG是一个综合指标，既考察价值，又兼顾成长性。PEG估值法适用于
成长型的公司

PEG策略：选择PEG最低的N支股票，代表潜力最大的
计算股票池中所有股票的PEG，选择PEG最小的N支股票调仓
***注意要过滤掉市盈率和收益增长率为负的股票
'''
from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    log.info('START')
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    g.security = get_index_stocks('000300.XSHG')
    g.N = 20
    g.q = query(valuation.code, valuation.pe_ratio, indicator.inc_net_profit_year_on_year).filter(valuation.code.in_(g.security))
    run_monthly(handle, 1)
def handle(context):
    
    # 得到code代码，市盈率pe，收益增长率G
    df = get_fundamentals(g.q)
    # 过滤掉市盈率和收益增长率为负的股票
    df = df[(df['pe_ratio'] > 0) & (df['inc_net_profit_year_on_year'] > 0)]
    # 计算PEG = PE / (100 * G)
    df['peg'] = df['pe_ratio'] / (100 * df['inc_net_profit_year_on_year'])
    # 找到PEG最小的N支的代码，转成列表存在to_hold中
    df = df.sort_values(by='peg', ascending=True)
    to_hold = df['code'][:g.N].values
    
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
    
   
   
   
