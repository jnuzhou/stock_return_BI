import pandas as pd

df1 = pd.read_csv('all_stock_daily_return.csv')
df2 = pd.read_csv('sse_daily_return.csv')

df = pd.concat([df1,df2[['sse_daily_return']]],axis = 1 )
df.to_csv('total_daily_return.csv',encoding='utf-8-sig')