#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd
import csv
import re
#from sys import platform as sys_pf
#if sys_pf == 'darwin':
import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from PIL import Image
from PIL import ImageTk as itk
from skimage.transform import rescale, resize, downscale_local_mean

pd.plotting.register_matplotlib_converters()

### TRADIER API - SPY ###

symbol = "spy"
API_URL = 'https://sandbox.tradier.com/v1/markets/quotes?symbols=%s' % symbol
headers = {"Accept":"application/json",
           "Authorization":"Bearer xxx"}

requests.get(API_URL, headers = headers)

download = requests.get(API_URL,headers=headers)
decoded_content = download.content.decode('utf-8')
cr = csv.reader(decoded_content.splitlines(), delimiter=',')
API_download = list(cr)
print (API_download)
results_SPY_close = API_download[0][4]
results_SPY_prevclose = API_download[0][17]

### REGEX ###
pattern = '\d+.\d+'
results_SPY_close = re.findall(pattern,results_SPY_close)[0]
results_SPY_prevclose = re.findall(pattern,results_SPY_prevclose)[0]

### Daily SPY change ###

SPY_delta = str(round((float(results_SPY_close) - float(results_SPY_prevclose)) / float(results_SPY_prevclose),3))
SPY_delta = SPY_delta +'%'


if float(results_SPY_close) - float(results_SPY_prevclose) > 0:
    change_SPY = "Positive"
elif float(results_SPY_close) == float(results_SPY_prevclose):
    change_SPY = "Before market open"
else:
    change_SPY = "Negative"

print(SPY_delta, results_SPY_close,results_SPY_prevclose,change_SPY)

### ALPHA VANTAGE API - EUR/RON - Monthly ###

s = 'EUR'
API2_URL = "https://www.alphavantage.co/query"
data = {"function":"FX_MONTHLY",
       "from_symbol":s,
       "to_symbol":"RON",
       "datatype":"csv",
       "apikey":"xxx"}

download = requests.get(API2_URL,data)
decoded_content = download.content.decode('utf-8')
cr = csv.reader(decoded_content.splitlines(), delimiter=',')
API2_download = list(cr)

### Monthly EUR/RON change ###

results_EUR_RON_today = float(API2_download[1][-1])
results_EUR_RON_last_month = float(API2_download[2][-1])

EUR_RON_delta = round(((results_EUR_RON_last_month - results_EUR_RON_today) / results_EUR_RON_today),4)
EUR_RON_delta = str(EUR_RON_delta) + '%'

if results_EUR_RON_today > results_EUR_RON_last_month :
    change_EUR_RON = "Negative"
else:
    change_EUR_RON = "Positive"
    
print(EUR_RON_delta, results_EUR_RON_today,results_EUR_RON_last_month,change_EUR_RON)

### ALPHA VANTAGE API - EUR/RON - Daily ###

s = 'EUR'
API2_URL = "https://www.alphavantage.co/query"
data = {"function":"FX_DAILY",
       "from_symbol":s,
       "to_symbol":"RON",
       "datatype":"csv",
       "apikey":"xxx"}

download = requests.get(API2_URL,data)
decoded_content = download.content.decode('utf-8')
cr = csv.reader(decoded_content.splitlines(), delimiter=',')
API2_download = list(cr)

### ALPHA VANTAGE API - EUR/RON - Daily ### --> Entering approximate monthly time series in pandas df

df1 = pd.DataFrame(API2_download,columns=['timestamp', 'open', 'high', 'low', 'close'])    
header = df1.iloc[0]
df1 = df1[1:31]
df1.rename(columns=header)
#df1.loc[[2]]
df1['close'] = df1['close'].astype(float)
df1['close'] = df1['close'] / df1.at[1,'close'] * 100
df1['low'] = df1['low'].astype(float)
df1['timestamp'] = df1['timestamp'].astype('datetime64')
#print (df1.at[1,'close'])

print(df1.head())

### Plot - EUR/RON - Daily

EURRON_Figure = plt.figure(figsize=(4,0.7), dpi=30)
plt.plot(df1['timestamp'], df1['close'],linewidth=2)
plt.axis('off')
#plt.show()

### ALPHA VANTAGE API - BTC/GBP ###

s = 'BTC'
API3_URL = "https://www.alphavantage.co/query"
data = {"function":"DIGITAL_CURRENCY_DAILY",
       "symbol":s,
       "market":"GBP",
       "datatype":"csv",
       "apikey":"xxx"}

download = requests.get(API3_URL,data)
decoded_content = download.content.decode('utf-8')
cr = csv.reader(decoded_content.splitlines(), delimiter=',')
API3_download = list(cr)
#print (API3_download)

### ALPHA VANTAGE API - BTC/GBP ### Entering approximate monthly time series in pandas df

df2 = pd.DataFrame(API3_download,columns=['timestamp', 'open (GBP)', 'high (GBP)', 'low (GBP)', 'close (GBP)', 'open (USD)', 'high (USD)', 'low (USD)', 'close (USD)', 'volume', 'market cap (USD)'])
header = df2.iloc[0]
df2 = df2[1:31]
df2.rename(columns=header)
#df2.loc[[2]]
df2['close (GBP)'] = df2['close (GBP)'].astype(float)
df2['close (GBP)'] = df2['close (GBP)'] / df2.at[1,'close (GBP)'] * 100
#df2['low'] = df1['low'].astype(float)
df2['timestamp'] = df2['timestamp'].astype('datetime64')
print(df2.head())

### Plot - BTC/GBP - Daily ###

BTCGBP_Figure = plt.figure(figsize=(4,0.7), dpi=30)
plt.plot(df2['timestamp'], df2['close (GBP)'], linewidth=2)
plt.axis('off')
#plt.savefig('BTC_GBP.png')  

### Daily BTC/GBP change ###

results_BTC_GBP_today = round(float(API3_download[1][4]),2)
results_BTC_GBP_yesterday = round(float(API3_download[2][4]),2)

BTC_GBP_delta = round(((results_BTC_GBP_today - results_BTC_GBP_yesterday) / results_BTC_GBP_today),3)
BTC_GBP_delta = str(BTC_GBP_delta) + '%'

if results_BTC_GBP_today > results_BTC_GBP_yesterday:
    change_BTC_GBP = "Positive"
else:
    change_BTC_GBP = "Negative"
    
print(BTC_GBP_delta, results_BTC_GBP_today,results_BTC_GBP_yesterday,change_BTC_GBP)

### Importing in dictionary ###

results_BTC_GBP_today = str(results_BTC_GBP_today)
results_BTC_GBP_today = '£ ' + results_BTC_GBP_today 

Daily_data = {'SPDR S&P500 ETF':results_SPY_close,
              'EUR/RON':results_EUR_RON_today,
              'BTC/GBP':results_BTC_GBP_today 
}
Daily_data_change = {"SPY_change":change_SPY,
                     'EUR/RON_change':change_EUR_RON,
                     'BTC/GBP_change':change_BTC_GBP
}
Daily_data_change_delta = {'SPY_delta':SPY_delta,
                          'EUR_RON_delta':EUR_RON_delta,
                          'BTC_GBP_delta':BTC_GBP_delta
}
Graphs_PNG = {'SPY': None,
             'EUR_RON':'EUR_RON.png',
             'BTC_GBP':'BTC_GBP.png'
}

### Tkinter wrapper creation ###

import tkinter as tk

root = tk.Tk()
root.title("Market Data Update")
r = 1

tk.Label(text='FX Daily Change', font = 'bold', width=15).grid(row=0,column=1)
tk.Label(text='Latest Close', font = 'bold', width=15).grid(row=0,column=2)
tk.Label(text='Monthly Movement', font = 'bold', width=15).grid(row=0,column=3)

for key1,key2,key3,key4 in zip(Daily_data,Daily_data_change,Daily_data_change_delta,Graphs_PNG):
    tk.Label(text=key1, relief=tk.RIDGE, width=15).grid(row=r,column=0)
    if Daily_data_change[key2] == "Negative":
        bg_color = "red"
    elif Daily_data_change[key2] == "Before market open":
        bg_color = "white"
    else:
        bg_color = "green"

    tk.Label(text=Daily_data_change_delta[key3], bg=bg_color, relief=tk.RIDGE, width=15).grid(row=r,column=1)
    tk.Label(text=Daily_data[key1], bg=bg_color, relief=tk.RIDGE, width=15).grid(row=r,column=2)
    r += 1

FigureA_canvas = FigureCanvasTkAgg(EURRON_Figure, master=root)
FigureA_canvas.get_tk_widget().grid(row=2,column=3,sticky='nswe')
FigureB_canvas = FigureCanvasTkAgg(BTCGBP_Figure, master=root)
FigureB_canvas.get_tk_widget().grid(row=3,column=3,sticky='nswe')
    
tk.mainloop()


# In[ ]:




