import requests

cookies = {
    '__cf_bm': 'DepNFG1Xs2CzJG8WbJ6akPtnuLSUnKEqGyHdNgEhYLs-1719913986-1.0.1.1-RptxBUpMlg0i3IzVp2J2FvzJTbWTQ7IMw_FdDOpm7B8Ho0vr9.jebEJk4N0PaTCBPEwmosHXjSgyRiMX4axbBg',
    'cf_clearance': 'wIY2kTsSkPU_3_cJmhOXSZGIs8adTJKpmohejt7yHVc-1719914004-1.0.1.1-21xM7twBA_3mjB5QNu5r9qCJwmk8Ejk5whgeLut9.dtZbM3H512QJYW4keYzWGLT0iepCSQYgTMguTeBBCN9Kw',
}

headers = {
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

params = {
    'appid': '762940',
    'cc': 'ch',
}

response = requests.get('https://steamdb.info/api/GetPriceHistory/', params=params, cookies=cookies, headers=headers)
rs = response.json()