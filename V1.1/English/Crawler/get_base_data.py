import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm
import random
import json
from retry import retry
from time import sleep
import requests
from lxml import etree
import re


# Generating the crawler using the crul tool
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': '__cf_bm=ce_6Xr65tVUZ1CHEdWbbo90_a5MN.530BYFSc_KGXTQ-1719646746-1.0.1.1-0nni3sD3DUpp5f_.XOT8JDKH3mGtm3D9w23XDUN54ot7fsEkYCAHv95swDaZEPrJ9imRJCQwmDQ.MSWeRzdwfw; cf_clearance=Ip2EgJJwVRGkf27bvR2t_UbvCSGrX9GWhs48oJmJi3w-1719646747-1.0.1.1-RF8tZ4OwmcXntwfjuVZ570hyM4_Y9y6T2XhYY45d1izWrhGw5vkRfaOIrORYQ6l_sm1F7arVwFpaSUzGUfj94A',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"126.0.6478.127"',
    'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"15.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}





myid = '782570'
# Get the first few columns of basic data, request request, lxml parsing
@retry(tries=3)
def get_data_1(myid, cookies1):
    response2 = requests.get('https://steamdb.info/app/{}/charts/'.format(myid), cookies=cookies1, headers=headers)
    # print(response2.status_code)
    myhtml2 = etree.HTML(response2.text)
    followers = myhtml2.xpath('//div[@class="row row-app-charts"]/div[1]//li//text()')
    followers_index = followers.index(' followers')
    followers = followers[followers_index-1]

    estimations = myhtml2.xpath('//div[@class="row row-app-charts"]/div[3]//li/strong/text()')
    estimations_name = myhtml2.xpath('//div[@class="row row-app-charts"]/div[3]//li/a/text()')
    if len(estimations) == 0:
        estimations = myhtml2.xpath('//div[@class="row row-app-charts"]/div[2]//li/strong/text()')
        estimations_name = myhtml2.xpath('//div[@class="row row-app-charts"]/div[2]//li/a/text()')

    try:
        PlayTracker_index = estimations_name.index('by PlayTracker')
        PlayTracker = estimations[PlayTracker_index]
    except Exception as e:
        PlayTracker = ''

    try:
        Gamalytic_index = estimations_name.index('by Gamalytic')
        Gamalytic = estimations[Gamalytic_index]
    except Exception as e:
        Gamalytic = ''

    try:
        VG_index = estimations_name.index('by VG Insights')
        VG = estimations[VG_index]
    except Exception as e:
        VG = ''

    return followers, PlayTracker, Gamalytic, VG





# Start execution, load game name
key_df = pd.read_excel('Namelist_no_duplicates.xlsx')

finish_key_word = []

shoudong_url = 'https://steamdb.info/app/1005410/'
option = ChromeOptions()
option.add_argument('--start-maximized')
option.add_argument('disable-infobars')
option.add_argument("--disable-blink-features=AutomationControlled")
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=option)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

# Automatic acquisition of cookies from the current browser
@retry(tries=3)
def get_chorme_cookies(myid):
    # driver.delete_all_cookies()
    driver.get('https://steamdb.info/app/{}/'.format(myid))
    cookie_list = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookiestr = ';'.join(item for item in cookie_list)
    cookies4 = {'Cookie': cookiestr}
    return cookies4



driver.get('https://steamdb.info/app/994730')




# The main core code, if there is an error, basically is blocked ip
#

cookies1= get_chorme_cookies('994730')
for id_index in tqdm(range(key_df.shape[0])):
    myid = str(key_df.iloc[id_index, 1])
    name = key_df.iloc[id_index, 0]
    if myid in finish_key_word:
        continue
    print(myid)
    # sleep(random.randint(5, 8))

    # myid = '1005410'

    followers, PlayTracker, Gamalytic, VG = get_data_1(myid, cookies1)
    # sleep(random.randint(15, 18))

    # genre, tag, category, owners = get_data_2(myid)


    # Saving data line by line
    with open('data_base.txt', 'a', encoding='gb18030') as f:
        one_data = [name, myid, followers, PlayTracker, Gamalytic, VG,
                    # owners, genre, tag, category
                    ]
        one_data = '$$%%'.join(one_data)
        one_data = one_data.replace('\n', '')
        f.write(one_data + '\n')
    f.close()
    finish_key_word.append(myid)
    sleep(random.randint(5, 13))

# Load in to excel
with open('data_base.txt', "r", encoding='gb18030') as f:
    data = f.read()

data = data.split('\n')
data = [i.split('$$%%') for i in data]

data_df = pd.DataFrame(data, columns=['Name', 'id',	'Follower',	'Owner PlayTracker',	'Owner Gamalytic',	'Owner VG Insights',
                                      # 'Owner Steamspy',	'Genre',	'Tags',	'Category'
                                      ]
)
data_df = data_df.dropna()
data_df = data_df.drop_duplicates(subset=['id'], keep='last').reset_index(drop=True)
data_df.to_excel('data_base.xlsx', index=False)
print('finish')
data_df.iloc[309:, :]

finish_key_word = list(data_df['id'].unique())
new_data_df = data_df.copy()
import numpy as np
for col in new_data_df.columns:
    new_data_df[col] = new_data_df[col].replace('', np.nan)
new_data_df = new_data_df.dropna(axis=0, how='any')
finish_key_word = list(new_data_df['id'].unique())