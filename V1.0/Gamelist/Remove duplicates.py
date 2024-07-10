import pandas as pd

# 载入数据
file_path = 'Namelist.xlsx'
data = pd.read_excel(file_path)

# 删除重复行
data_no_duplicates = data.drop_duplicates()

# 保存至新文件
cleaned_file_path = 'Namelist_no_duplicates.xlsx'
data_no_duplicates.to_excel(cleaned_file_path, index=False)

print("Duplicates have been removed and the cleaned data is saved to Namelist_no_duplicates.xlsx")
