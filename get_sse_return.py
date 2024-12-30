import yfinance as yf
from datetime import datetime, timedelta
import json
import pytz
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体为SimHei
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


# 获取三年前的日期，并转换为 tz-aware datetime 对象
end_date = datetime.now().date()
start_date = (datetime.now() - timedelta(days=3*365)).date()

# 转换为 tz-aware datetime 对象，使用中国标准时间
tz = pytz.timezone('Asia/Shanghai')
start_date = tz.localize(datetime.combine(start_date, datetime.min.time()))
end_date = tz.localize(datetime.combine(end_date, datetime.min.time()))

# 获取上证指数的历史数据
sse_ticker = yf.Ticker('000001.SS')
sse_hist_data = sse_ticker.history(start=start_date, end=end_date)


if not sse_hist_data.empty:
    sse_initial_price = sse_hist_data['Close'].iloc[0]
    sse_total_values = sse_hist_data['Close']
    sse_daily_values = sse_total_values / sse_initial_price
else:
    print("无法获取上证指数数据")
    sse_daily_values = None

dates = sse_hist_data.index
df = pd.DataFrame({'sse_daily_return':sse_daily_values},index = dates)
df.to_csv('sse_daily_return.csv',encoding='utf-8-sig',index=dates)



