# Steam独立游戏数据爬虫与分析项目

## 项目简介

本项目旨在爬取Steam上的独立游戏数据，并进行数据分析。我们主要从SteamDB和SteamSpy两个网站获取数据，包括玩家拥有量、各地区价格、游戏ID等数据标签。通过数据分析，找出误差较小的玩家拥有量数据源，并给出最频繁的定价策略分析。分析的结论是：PlayTracker的玩家拥有量最不准确。我们还给出了以美元价格为标的情况下的不同价格游戏的最频繁定价策略分析。


## 文件说明

### 数据分析

- `Analysis.ipynb`：数据分析的Jupyter Notebook，包含数据处理与分析过程。
- `ConvertNumber.ipynb`：数据预处理和数字格式转换的Jupyter Notebook，帮助处理数据中的数值格式。
- `DataSample.xlsx`：原始数据样本。
- `DataSample_converted.xlsx`：转换后的数据样本。
- `cleaned_data.xlsx`：清洗后的数据文件。
- `最频繁的定价策略.txt`：分析结果，包含最频繁的定价策略总结。
- `老数据`：数据量更小的测试数据集。

### 数据爬虫

- `chromedriver.exe`：Chrome浏览器驱动，用于爬虫。
- `data_combine.py`：数据合并脚本，将多个数据源的数据进行合并处理。
- `get_base_data.py`：获取基础数据的爬虫脚本。
- `get_base_steamspy.py`：从SteamSpy获取基础数据的爬虫脚本。
- `get_price.py`：获取价格数据的爬虫脚本。
- `test.py`：测试脚本，验证爬虫是否工作正常。
- `游戏名ID检索（爬虫用）`：steamID和游戏名一一对应的目录。
- `数据`：爬取的数据，名为data的数据是合并后的数据。

