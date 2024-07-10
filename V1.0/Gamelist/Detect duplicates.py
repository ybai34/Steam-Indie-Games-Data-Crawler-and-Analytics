# 载入数据
import pandas as pd

file_path = 'Namelist.xlsx'
data = pd.read_excel(file_path)

# 检测重复行
duplicate_rows = data[data.duplicated()]

# 展示重复行
print(duplicate_rows)
