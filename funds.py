from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import time
df = pd.read_csv('架上基金一覽表_20210331.csv')
filter_b=(df['AUM類別'] =='B-債券型')
df_B = df[filter_b] 
filter_e=(df['AUM類別'] =='E-股票型')
df_E = df[filter_e] 
filter_f=(df['AUM類別'] =='F-組合型')
df_F = df[filter_f] 
filter_i=(df['AUM類別'] =='I-指數型')
df_I = df[filter_i] 
filter_m=(df['AUM類別'] =='M-貨幣型')
df_M = df[filter_m] 
filter_o=(df['AUM類別'] =='O-其他型')
df_O = df[filter_o] 
filter_w=(df['AUM類別'] =='W-平衡型')
df_W = df[filter_w] 


# print(df_B.iloc[:,17]) #根據基金代號取出，相同AUM類別之基金
# print(df.index) # 印出所有的基金代號
# print(df_B.loc['84U']) # 印出單一基金的個別資料
# print(df_B.loc['84U'][8]) # 印出單一基金的手續費

# print(df.shape)
# print(matplotlib.matplotlib_fname()) 

df_net1 = pd.read_csv('基金淨值2014.csv')
df_net2 = pd.read_csv('基金淨值2015.csv')
df_net3 = pd.read_csv('基金淨值2016.csv')
df_net4 = pd.read_csv('基金淨值2017.csv')
df_net5 = pd.read_csv('基金淨值2018.csv')
df_net6 = pd.read_csv('基金淨值201901至201909.csv')
df_net7 = pd.read_csv('基金淨值201910至202006.csv')
df_net8 = pd.read_csv('基金淨值202007至202103.csv')
frame = [df_net1,df_net2,df_net3,df_net4,df_net5,df_net6,df_net7,df_net8]
df_allnet = pd.concat(frame)

df_allnet.rename(columns={'參考日期(淨值)':'date'}, inplace = True)
df_code=df_allnet.iloc[:,0:3]

df_allnet.set_index("date",inplace=True)
df_allnet.index=pd.to_datetime(df_allnet.index,format='%Y-%m-%d')

# W-平衡型 抓出每一檔歷年淨值

tim = df_allnet.index
tim = pd.Series(tim)
tim=sorted(list(set(tim)))

df2=pd.DataFrame(pd.np.empty((0,2566)))  
df2.columns=tim

for c in df_W.基金代號:
    cnt=0
    for i in df_allnet.iloc[:,0]:
        if c==i:
            print(c,df_allnet.iloc[cnt,1],df_allnet.iloc[cnt,4])
            # print(c,df_allnet.iloc[cnt,1:2])
            # print(df_allnet.iloc[cnt,1])
            # df1 = pd.DataFrame()
        if cnt >70000000:
            break
        cnt+=1




