# 目标
# 设置股票池为沪深300的所有成份股；
# 如果当前股价小于10元/股且当前不持仓，买入；
# 如果当前股价比比买入时上涨了25%，则清仓止盈；
# 如果当前股价比比买入时下跌了10%，则清仓止损。

from jqdata import *

def initialize(context):
    # 设置基准收益
    set_benchmark('000300.XSHG')
    # 1.设置股票池为沪深300的所有成份股；
    g.security = get_index_stocks('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    log.info('START')
    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')

# 每天的行为
def handle_data(context, data):
    
    # 先看要买哪些股票，把可用资金平均分给这些股票的购买
    
    tobuy = [] # 要买哪些股票
    for stock in g.security:
        p = get_current_data()[stock].day_open
        if stock in context.portfolio.positions:
            amount = context.portfolio.positions[stock].total_amount
            cost = context.portfolio.positions[stock].avg_cost
        else:
            amount = 0
            cost = 0
        # 2.如果当前股价小于10元/股且当前不持仓，把这支股票定为可买入；
        if p <= 10.0 and amount == 0:
            tobuy.append(stock)
        # 3. 如果当前股价比比买入时上涨了25%，则清仓止盈；
        if amount > 0 and p >= cost * 1.25:
            order_target(stock, 0)
        # 4.如果当前股价比比买入时下跌了10%，则清仓止损;
        if amount > 0 and p <= cost * 0.9:
            order_target(stock, 0)
    
    # 一般先卖出再买入
    cash_per_stock = context.portfolio.available_cash / len(tobuy)
    for stock in tobuy:
        order_value(stock, cash_per_stock) # 买入股票
    
    












