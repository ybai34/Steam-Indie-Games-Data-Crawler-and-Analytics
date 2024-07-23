import pandas as pd

data_base = pd.read_excel('data_base.xlsx')
data_base_steampy = pd.read_excel('data_base_steampy.xlsx')



data_price = pd.read_excel('data_price.xlsx')
data_price['id'].value_counts()
data_price_new = pd.crosstab(data_price['id'], data_price['diqu'], data_price['price'], aggfunc='sum')
data_price_new = data_price_new.rename(columns={'tw':'Taiwan Dollar', 'ru':'Russian Ruble', 'br':'Brazilian Real', 'kz':'Kazakhstani Tenge', 'ua':'Ukrainian Hryvnia',
        'in':'Indian Rupee', 'id':'Indonesian Rupiah', 'za':'South African Rand', 'co':'Colombian Peso', 'cl':'Chilean Peso',
        'vn':'Vietnamese Dong', 'ph':'Philippine Peso', 'my':'Malaysian Ringgit', 'th':'Thai Baht', 'sa':'Saudi Riyal',
        'cn':'Chinese Yuan', 'pk':' South Asia - USD', 'uy':'Uruguayan Peso', 'pe':'Peruvian Sol', 'jp':'Japanese Yen',
        'mx':'Mexican Peso', 'az':'CIS - U.S. Dollar', 'kw':'Kuwaiti Dinar', 'hk':'Hong Kong Dollar', 'no':'Norwegian Krone',
        'qa':'Qatari Riyal', 'nz':'New Zealand Dollar', 'sg':'Singapore Dollar', 'kr':'South Korean Won', 'ae':'U.A.E. Dirham',
        'ca':'Canadian Dollar', 'cr':'Costa Rican Colon', 'pl':'Polish Zloty', 'au':'Australian Dollar', 'eu':' Euro', 'il':' Israeli New Shekel',
        'us':'U.S. Dollar', 'ar':'LATAM - U.S. Dollar', 'tr':'MENA - U.S. Dollar', 'uk':'British Pound', 'ch':'Swiss Franc'})
data_price_new = data_price_new.reset_index()

data = pd.merge(data_base, data_base_steampy, how='outer', on='id')
data = data.merge(data_price_new, how='outer', on='id')

data.to_excel('data.xlsx', index=False)
print('finish')
