import matplotlib.pyplot as plt
import os 
import yfinance as yf
from datetime import datetime, timedelta
import json
import pytz
from tqdm import tqdm
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体为SimHei
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

json_file_path = 'nested_list.json'

# 从 JSON 文件读取字典
if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        nested_list = json.load(json_file)
else:
    print("Nested list file not found.")
    nested_list = {}


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
print(sse_hist_data)

if not sse_hist_data.empty:
    sse_initial_price = sse_hist_data['Close'].iloc[0]
    sse_total_values = sse_hist_data['Close']
    sse_daily_values = sse_total_values / sse_initial_price
else:
    print("无法获取上证指数数据")
    sse_daily_values = None

dates = sse_hist_data.index



for symbol, daily_values in tqdm(nested_list.items(), desc="Processing stocks"):

    if daily_values is not None and sse_daily_values is not None:
        # 将 daily_values 转换为 pandas Series 并重新索引，以确保与 dates 对齐
        daily_values_series = pd.Series(daily_values, index=dates[:len(daily_values)])
        daily_values_series = daily_values_series.reindex(dates, method='ffill')

    if daily_values is not None and sse_daily_values is not None:
        plt.figure(figsize=(12, 6))
        plt.plot(dates, daily_values_series, label=f'{symbol} 收益率')
        plt.plot(dates, sse_daily_values, label='上证指数 收益率', linestyle='--')
        plt.xlabel('日期')
        plt.ylabel('收益率')
        plt.title(f'{symbol} 收益率曲线 vs 上证指数')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'./daily_return_picture/returns_{symbol}.png')
        plt.close()

print("所有收益率曲线图已保存")