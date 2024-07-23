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
import random






# 地区
diqu = {'tw':'Taiwan Dollar', 'ru':'Russian Ruble', 'br':'Brazilian Real', 'kz':'Kazakhstani Tenge', 'ua':'Ukrainian Hryvnia',
        'in':'Indian Rupee', 'id':'Indonesian Rupiah', 'za':'South African Rand', 'co':'Colombian Peso', 'cl':'Chilean Peso',
        'vn':'Vietnamese Dong', 'ph':'Philippine Peso', 'my':'Malaysian Ringgit', 'th':'Thai Baht', 'sa':'Saudi Riyal',
        'cn':'Chinese Yuan', 'pk':' South Asia - USD', 'uy':'Uruguayan Peso', 'pe':'Peruvian Sol', 'jp':'Japanese Yen',
        'mx':'Mexican Peso', 'az':'CIS - U.S. Dollar', 'kw':'Kuwaiti Dinar', 'hk':'Hong Kong Dollar', 'no':'Norwegian Krone',
        'qa':'Qatari Riyal', 'nz':'New Zealand Dollar', 'sg':'Singapore Dollar', 'kr':'South Korean Won', 'ae':'U.A.E. Dirham',
        'ca':'Canadian Dollar', 'cr':'Costa Rican Colon', 'pl':'Polish Zloty', 'au':'Australian Dollar', 'eu':' Euro', 'il':' Israeli New Shekel',
        'us':'U.S. Dollar', 'ar':'LATAM - U.S. Dollar', 'tr':'MENA - U.S. Dollar', 'uk':'British Pound', 'ch':'Swiss Franc'}






# 先启动浏览器，手动过掉cf验证，尝试打开https://steamdb.info/app/1005410/，进入环境。
# 这一步，要在chorme里新打开一个窗口，手动输入这个shoudong_url，等过掉验证后，再在主窗口打开shoudong_url
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



# 获取浏览器的cookies
@retry(tries=3)
def get_chorme_cookies(myid):
    driver.delete_all_cookies()
    driver.get('https://steamdb.info/app/{}/'.format(myid))
    cookie_list = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookiestr = ';'.join(item for item in cookie_list)
    cookies4 = {'Cookie': cookiestr}
    return cookies4
# 获取一个地方的价格
@retry(tries=3)
def get_data_3(myid, diqu_i, cookies4, headers2):
    params = {
        'appid': myid,
        'cc': diqu_i,
    }
    try:
        response4 = requests.get('https://steamdb.info/api/GetPriceHistory/', params=params, cookies=cookies4,
                                 headers=headers2, timeout=20)
        if response4.status_code == 404:
            return ''
        rs = response4.json()
        rs = rs['data']['history']
    except Exception as e:
        print(response4.status_code, e)

    rs.reverse()
    for rs_i in rs:
        if rs_i['d'] == 0:
            price = rs_i['f']
            break
    return price

headers2 = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': '__cf_bm=DepNFG1Xs2CzJG8WbJ6akPtnuLSUnKEqGyHdNgEhYLs-1719913986-1.0.1.1-RptxBUpMlg0i3IzVp2J2FvzJTbWTQ7IMw_FdDOpm7B8Ho0vr9.jebEJk4N0PaTCBPEwmosHXjSgyRiMX4axbBg; cf_clearance=wIY2kTsSkPU_3_cJmhOXSZGIs8adTJKpmohejt7yHVc-1719914004-1.0.1.1-21xM7twBA_3mjB5QNu5r9qCJwmk8Ejk5whgeLut9.dtZbM3H512QJYW4keYzWGLT0iepCSQYgTMguTeBBCN9Kw',
    'priority': 'u=1, i',
    'referer': 'https://steamdb.info/app/762940/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"126.0.6478.127"',
    'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"15.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


driver.implicitly_wait(40)
# 开始执行
data_base = pd.read_excel('data_base.xlsx')
finish_index = []

for id_index in tqdm(range(data_base.shape[0])):

    myid = data_base.iloc[id_index, 1]
    if myid in [698780, 2596760, 2408630]:
        continue
    if str(myid) in finish_index:
        continue

    print(myid)

    cookies4 = get_chorme_cookies(myid)
    sleep(random.randint(2, 10))
    headers2['referer'] = 'https://steamdb.info/app/{}/'.format(myid)
    for diqu_i in tqdm(list(diqu.keys())):
        if str(myid) + '_' + diqu_i in finish_index:
            continue
        print(diqu_i)

        try:
            price = get_data_3(myid, diqu_i, cookies4, headers2)
        except Exception as e:
            print(e)
            sleep(20)
            cookies4 = get_chorme_cookies(myid)
            continue

        # 逐条保存数据
        with open('data_price.txt', 'a', encoding='gb18030') as f:
            one_data = [str(myid), diqu_i, price]
            one_data = '$$%%'.join(one_data)
            one_data = one_data.replace('\n', '')
            f.write(one_data + '\n')
            f.close()
        finish_index.append(str(myid) + '_' + diqu_i)
        sleep(random.randint(1, 4))

    finish_index.append(myid)



# 加载进来转换成excel
with open('data_price.txt', "r", encoding='gb18030') as f:  # 打开文件
    data = f.read()

data = data.split('\n')
data = [i.split('$$%%') for i in data]


data_df = pd.DataFrame(data, columns=['id',	'diqu',	'price'])
data_df = data_df.dropna()
data_df = data_df.drop_duplicates()
data_df.to_excel('data_price.xlsx', index=False)


finish_index = data_df.apply(lambda funp: str(funp['id']) + '_' + funp['diqu'], axis=1).to_list()
finish_name = data_df['id'].value_counts().reset_index()
finish_name = finish_name[finish_name['count']==41]['id'].to_list()
finish_index = finish_index + finish_name
print('finish')
