import akshare as ak
import pandas as pd
import backtrader as bt

history = ak.stock_zh_a_hist(symbol="000002", period="daily", start_date="20101103",
                             end_date="20201116")
history["日期"] = pd.to_datetime(history["日期"])
history.set_index("日期", inplace=True)
print(history.index)

data = bt.feeds.PandasData()

cerebro = bt.Cerebro()
cerebro.adddata(data)
# 初始资金 100,000,000
cerebro.broker.setcash(100000000.0)
# 佣金，双边各 0.0003
cerebro.broker.setcommission(commission=0.0003)
# 滑点：双边各 0.0001
cerebro.broker.set_slippage_perc(perc=0.0001)

cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='pnl') # 返回收益率时序数据
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn') # 年化收益率
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio') # 夏普比率
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown') # 回撤

# 通过继承 Strategy 基类，来构建自己的交易策略子类
class MyStrategy(bt.Strategy):
    # 定义我们自己写的这个 MyStrategy 类的专有属性
    def __init__(self):
        '''必选，策略中各类指标的批量计算或是批量生成交易信号都可以写在这里'''
        pass
    # 构建交易函数: 策略交易的主体部分
    def next(self):
        '''必选，在这里根据交易信号进行买卖下单操作'''
        pass



cerebro.addstrategy(MyStrategy)

result = cerebro.run()

