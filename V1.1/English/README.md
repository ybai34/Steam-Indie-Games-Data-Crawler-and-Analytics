# Steam Indie Games Data Crawler and Analysis Project

## Project Overview

This project aims to crawl and analyze data of indie games on Steam. We primarily gather data from SteamDB and SteamSpy, including player ownership, regional prices, game IDs, and other data tags. Through data analysis, we aim to identify the most accurate sources for player ownership data and provide an analysis of the most frequent pricing strategies. The analysis concludes that PlayTracker has the least accurate player ownership. We also give an analysis of the most frequent pricing strategies for games with different prices in the case of dollar prices.


## File Descriptions

### Crawler

- `chromedriver.exe`: Chrome browser driver used for web crawler.
- `data_combine.py`: Script to combine data from multiple sources.
- `get_base_data.py`: Script to fetch basic data.
- `get_base_steamspy.py`: Script to fetch data from SteamSpy.
- `get_price.py`: Script to fetch pricing data.
- `test.py`: Test script to verify the crawler is working correctly.
- `Game ID Menu (for crawler)`: A directory where steamID and game name correspond one to one.
- `Data`: The crawled data.



### Data Analysis

- `Analysis.ipynb`: Jupyter Notebook for data analysis, containing data processing and analysis steps.
- `ConvertNumber.ipynb`: Jupyter Notebook for converting numerical data formats.
- `DataSample.xlsx`: Sample of raw data.
- `DataSample_converted.xlsx`: Sample of converted data.
- `cleaned_data.xlsx`: Cleaned data file.
- `Most Frequent Pricing Strategies.txt`: The results of the analysis, containing a summary of the most frequent pricing strategies.
- `Old Data`: Smaller dataset for testing.




