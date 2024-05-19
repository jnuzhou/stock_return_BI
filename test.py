import pandas as pd

# 使用 Series 列表创建 DataFrame
data = [
    pd.Series([1, 2, 3]),
    pd.Series([4, 5, 6])
]
df = pd.DataFrame(data,index = [1,2])
df.columns = ['a','b','c']
print(df)