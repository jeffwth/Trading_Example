# 双均线策略
# ma5、ma10:短期，日均线；
# ma30、ma60:中期，季均线；
# ma120、ma240:长期，年均线；
# 金叉：短期均线上穿长期均线，买入信号
# 死叉：短期均线下穿长期均线，卖出信号
from jqdata import *

# 初始化函数，设定基准等等
def initialize(context):
    # 初始函数中最基本的设置：
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    # 输出内容到日志 log.info()
    log.info('START')
    
    g.security = ['601318.XSHG']
    g.p1 = 5
    g.p2 = 10
    

def handle_data(context, data):
    for stock in g.security:
        # 金叉：ma5大于ma10，且不持仓
        # 死叉：ma5小雨ma10，且持仓
        df = attribute_history(stock,g.p2)
        ma10 = df['close'].mean()
        ma5 = df['close'][-5:].mean()
        
        # 死叉，全部卖出
        if ma10 > ma5 and stock in context.portfolio.positions:
            order_target(stock, 0)
        
        # 金叉，用80%可用的钱买入
        if ma5 > ma10 and stock not in context.portfolio.positions:
            order_value(stock, context.portfolio.available_cash * 0.8)
        
    record(ma5 = ma5, ma10 = ma10)  
        
        
        
        
        
        
        
        
        
        
        
        
        
        
