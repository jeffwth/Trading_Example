'''
布林带Bollinger Band由三条轨道线组成，其中上下两条线分别可以看成是价格的压力线和
支撑线，在两条线之间是一条价格平行线

计算公式：
中间线：20日均线
up线：20日均线 + N * Std(20日收盘价)
down线：20日均线 - N * Std(20日收盘价)

股价突破阻力线(up线)卖出，股价跌破支撑线(down线)买入

策略主要研究：N的取值，布林带宽度
'''
from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    log.info('START')
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    
    g.security = '600036.XSHG'
    g.M = 20
    g.k = 2
    
def handle_data(context, data):
    sr = attribute_history(g.security, g.M)['close']
    ma = sr.mean()
    up = ma + g.k * sr.std()
    down = ma - g.k * sr.std()
    p = get_current_data()[g.security].day_open
    
    cash = context.portfolio.available_cash
    if p < down and g.security not in context.portfolio.positions:
        order_value(g.security, cash)
    elif p > up and g.security in context.portfolio.positions:
        order_target(g.security, 0)
    
    
    
    
    
    
    
    
    
    
