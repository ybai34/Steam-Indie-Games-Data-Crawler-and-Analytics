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




# 在完成登陆后，使用crul工具l进行生成
cookies2 = {
    'cf_chl_rc_ni': '1',
    'PHPSESSID': 'hkllvasmrren9ur57lbr6gbmce',
    '_ga': 'GA1.2.314424286.1719663295',
    '_gid': 'GA1.2.52811692.1719663295',
    '_gat': '1',
    'cf_clearance': 'CMoXx6pFC4bHiHVp7q9zNo_oikYKFD8p5eQUt8xvybs-1719663296-1.0.1.1-i_8Kp8E72Tp0FZJmf_RIUNWJq329A2XtAbtdqedhWsLXaFNdKxVCHKzUfBg6Lyh0FDWFhz8t0WIXlhW8SkIoFw',
    '_ga_92568JHCDC': 'GS1.2.1719663296.1.1.1719663296.0.0.0',
    'SteamSpySession': '51d237e294a0fda1c467146707e89afc01bf6f75',
}

headers2 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'cf_chl_rc_ni=1; PHPSESSID=hkllvasmrren9ur57lbr6gbmce; _ga=GA1.2.314424286.1719663295; _gid=GA1.2.52811692.1719663295; _gat=1; cf_clearance=CMoXx6pFC4bHiHVp7q9zNo_oikYKFD8p5eQUt8xvybs-1719663296-1.0.1.1-i_8Kp8E72Tp0FZJmf_RIUNWJq329A2XtAbtdqedhWsLXaFNdKxVCHKzUfBg6Lyh0FDWFhz8t0WIXlhW8SkIoFw; _ga_92568JHCDC=GS1.2.1719663296.1.1.1719663296.0.0.0; SteamSpySession=51d237e294a0fda1c467146707e89afc01bf6f75',
    'priority': 'u=0, i',
    'referer': 'https://steamspy.com/login/',
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
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}



myid = '994730'


# 获取steamspy的数据
@retry(tries=3)
def get_data_2(myid):
    response3 = requests.get('https://steamspy.com/app/{}'.format(myid), cookies=cookies2, headers=headers2)
    myhtml3 = etree.HTML(response3.text)
    steamspy = myhtml3.xpath('//div[@class="col-md-4 no-padding"]//p//text()')
    steamspy = [str(i) for i in steamspy]
    genre_index = steamspy.index('Genre:')
    languages_index = steamspy.index('Languages:')
    genre = ''.join(steamspy[genre_index + 1: languages_index]).strip()
    tag_index = steamspy.index('Tags:')
    category_index = steamspy.index('Category:')
    tag = ''.join(steamspy[tag_index + 1:category_index]).strip()
    release_index = steamspy.index('Release date')
    category = ''.join(steamspy[category_index + 1:release_index]).strip()
    owners_index = steamspy.index('Owners')
    owners = steamspy[owners_index + 1]
    owners = owners.replace(',', '')
    owners = re.findall('\d+', owners)
    owners = owners[0]
    return genre, tag, category, owners












# url = 'https://steamdb.info/app/1005410/'
# cookies1 = get_chorme_cookies(url)

shoudong_url = 'https://steamspy.com/app/1005410/'
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

@retry(tries=3)
def get_chorme_cookies(myid):
    # driver.delete_all_cookies()
    driver.get('https://steamspy.com/app/{}/'.format(myid))
    cookie_list = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookiestr = ';'.join(item for item in cookie_list)
    cookies4 = {'Cookie': cookiestr}
    return cookies4

key_df = pd.read_excel('Namelist_no_duplicates.xlsx')
driver.get('https://steamspy.com/app/1005410/')



finish_index = []

cookies2= get_chorme_cookies('1005410')


for id_index in tqdm(range(key_df.shape[0])):

    myid = key_df.iloc[id_index, 1]
    myid = str(myid)
    if myid in finish_index:
        continue
    # myid = '977880'
    try:
        genre, tag, category, owners = get_data_2(myid)
        print(myid, owners)
    except Exception as e:
        print(myid, e)
        continue
    # if id_index > 10:
    #     break

    # 逐条保存数据
    with open('data_base_steampy.txt', 'a', encoding='gb18030') as f:
        one_data = [str(myid),
                    owners, genre, tag, category
                    ]
        one_data = '$$%%'.join(one_data)
        one_data = one_data.replace('\n', '')
        f.write(one_data + '\n')
    f.close()
    finish_index.append(myid)
    sleep(random.randint(1, 5))

# 加载进来转换成excel
with open('data_base_steampy.txt', "r", encoding='gb18030') as f:  # 打开文件
    data = f.read()

data = data.split('\n')
data = [i.split('$$%%') for i in data]

data_df = pd.DataFrame(data, columns=['id',
                                      'Owner Steamspy',	'Genre',	'Tags',	'Category'
                                      ]
)
data_df = data_df.dropna()
data_df = data_df.drop_duplicates('id')
data_df.to_excel('data_base_steampy.xlsx', index=False)
print('finish')
key_df['id'].nunique()
finish_index = list(data_df['id'].unique())
data_df['id'].value_counts()
data_df[data_df['id']=='774361']['Owner Steamspy']