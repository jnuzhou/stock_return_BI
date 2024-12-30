import pandas as pd 
import yfinance as yf
import json
import os
from datetime import datetime,timedelta
import pytz
from tqdm import tqdm


json_file_path = 'stock_dict.json'

# 从 JSON 文件读取字典
if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        stock_dict = json.load(json_file)
else:
    print("Stock dictionary file not found.")


end_date = datetime.now().date()
start_date = (datetime.now() - timedelta(days=3*365)).date()

# 转换为 tz-aware datetime 对象，使用中国标准时间
tz = pytz.timezone('Asia/Shanghai')
start_date = tz.localize(datetime.combine(start_date, datetime.min.time()))
end_date = tz.localize(datetime.combine(end_date, datetime.min.time()))


returns_dict = {}
daily_values_dict = {}
daily_values_df = pd.DataFrame()
for symbol in tqdm(stock_dict.keys(), desc="Processing stocks"):

    # 判断股票是上海交易所还是深圳交易所
    if symbol.startswith('6'):
        symbol_with_suffix = symbol + '.SS'  # 上海交易所
    else:
        symbol_with_suffix = symbol + '.SZ'  # 深圳交易所

    ticker = yf.Ticker(symbol_with_suffix)
    
    # 获取三年历史数据
    hist_data = ticker.history(start=start_date, end=end_date)
    
    # 获取分红数据
    div_data = ticker.dividends[start_date:end_date]


    div_data.reindex(hist_data.index, fill_value=0).cumsum()

    # 计算总收益
    if not hist_data.empty:
        initial_price = hist_data['Close'].iloc[0]
        final_price = hist_data['Close'].iloc[-1]
        total_dividends = div_data.sum()
        
        total_return = (final_price - initial_price + total_dividends) / initial_price
        returns_dict[symbol] = total_return


        # 计算每天的总价值/初始金额 ，数据格式为Series
        daily_values = (hist_data['Close'] + div_data.reindex(hist_data.index, fill_value=0).cumsum()) / initial_price   
        daily_values_dict[symbol] = daily_values
        
        df = pd.DataFrame({f'{stock_dict[symbol]}':daily_values},index = hist_data.index)
        daily_values_df = pd.concat([daily_values_df,df],axis=1)
        
         
        
    else:
        returns_dict[symbol] = None
        daily_values_dict[symbol] = None





# 将 daily_values_dict 转换为嵌套列表
nested_list = {symbol: daily_values.tolist() if daily_values is not None else None for symbol, daily_values in daily_values_dict.items()}

for symbol, total_return in returns_dict.items():
    if total_return is not None:
        print(f"股票名称: {stock_dict[symbol]}, 总收益: {total_return:.2%}")
    else:
        print(f"股票名称: {stock_dict[symbol]}, 无法获取数据")

for symbol, daily_values in daily_values_dict.items():
    if daily_values is not None:
        daily_values.to_csv(f'./daily_values/daily_values_{symbol}.csv')

# 保存收益结果到 JSON 文件
with open('returns_dict.json', 'w', encoding='utf-8') as json_file:
    json.dump(returns_dict, json_file, ensure_ascii=False, indent=4)

# 保存嵌套列表到 JSON 文件
with open('nested_list.json', 'w', encoding='utf-8') as json_file:
    json.dump(nested_list, json_file, ensure_ascii=False, indent=4)

print("收益结果已保存至 'returns_dict.json' 和 'nested_list.json'")

if daily_values_df is not None:
    daily_values_df.to_csv(f'all_stock_daily_return.csv',encoding='utf-8-sig')


