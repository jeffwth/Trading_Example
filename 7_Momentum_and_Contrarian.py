'''
动量策略：如果一只股票在前一段时间表现较好，那么下一段时期该股票仍有
良好的表现；
反转策略：如果一只股票在前一段时间表现不好，那么下一段时期该股票将会
反转，即表现变好

计算股票池中所有股票在前一段时间的收益率
选择收益率最大/最小的N支调仓
两种思想
判断是动量>反转还是反转>动量，会影响其他的策略
'''

# 导入函数
from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    log.info('START')
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    g.N = 10
    run_monthly(handle, 1)
    
def handle(context):
    
    stocks = get_index_stocks('000300.XSHG')
    
    # history获取stocks 30天的收盘价
    df_close = history(30, field='close', security_list=list(stocks)).T
    # 收益率 (最后一天的收盘价-30天之前的价格)/30天之前的价格 
    df_close['ret'] = (df_close.iloc[:,-1]-df_close.iloc[:,0]) / df_close.iloc[:,0]
    # 收益率排序 降序，选择收益最大的，动量策略
    sorted_stocks = df_close.sort_values(by='ret', ascending=False).index
    # 选择收益最小的，反转策略
    # sorted_stocks = df_close.sort_values(by='ret', ascending=True).index
    to_hold = sorted_stocks[:g.N]
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
    
   
   
   
