import math
import requests
from scipy import stats

'''
ahr999囤币指标:
计算方式：ahr999指标 =（比特币价格/200日定投成本）*（比特币价格/指数增长估值）。
其中指数成长估值为币价和币龄的拟合结果，本指数拟合方法为每月对历史数据进行拟合。

指标说明：该指标由微博用户ahr999创建，辅助比特币定投用户结合择机策略做出投资决策。 
该指标隐含了比特币短期定投的收益率及比特币价格与预期估值的偏离度。 
从长期来看，比特币价格与区块高度呈现出一定的正相关，同时借助定投方式的优势，短期定投成本大都位于比特币价格之下。 
因此，当比特币价格同时低于短期定投成本和预期估值时增大投资额，能增大用户收益的概率。 
根据指标回测，当指标低于0.45时适合抄底，在0.45和1.2区间内适合定投BTC，高于该区间意味着错过最佳定投时期。
'''


def ahr999():
    url = 'https://api-pub.bitfinex.com/v2/candles/trade:1D:tBTCUSD/hist?start=1577836800000&end=1714121440000&sort=1&limit=10000'

    r = requests.get(url)
    data = r.json()
    print("data len:", len(data))
    lows = []

    for item in data:
        low = item[4]
        lows.append(low)
        if len(lows) > 200:
            lows.pop(0)
        geomean = stats.gmean(lows)
        day = (item[0] / 1000 - 1230940800) / (24 * 60 * 60)
        coinIndex = 10 ** (5.84 * math.log(day, 10) - 17.01)
        ahr999 = (low / geomean) * (low / coinIndex)
        print(item, ahr999, day, coinIndex, geomean)


if __name__ == '__main__':
    ahr999()
