import requests
import time
import execjs
import pandas as pd
import numpy as np


# df_high =pd.read_csv('worth_org.csv')
df_high_train = pd.read_csv('high_train.csv')
df_high =pd.read_csv('high.csv')

# df_high_train['668'] = df_high['668']

df_high_train = df_high_train.replace(0,np.nan)
df_high_train = df_high_train.dropna()

df1 = df_high_train.T

fileTrain = 'Train1.csv'
train = np.array(df1.loc['A07':'IN1'].index)
fileTest = 'Test1.csv'
Test = np.array(df1.loc['JA2':'JA2'].index)


Worth_file = open(fileTrain, 'w')
for code in train:
    try:
        worth = df1.loc[code]
        print(worth)
    except:
        continue    
    if len(worth) > 0:
        Worth_file.write(",".join(list(map(str, worth))))
        Worth_file.write("\n")
        print('{} data downloaded'.format(code))
Worth_file.close()

worth_test_file = open(fileTest, 'w')
for code in Test:
    worth = df1.loc[code]
    if len(worth) > 0:
        worth_test_file.write(",".join(list(map(str, worth))))
        worth_test_file.write("\n")
        print('{} data downloaded'.format(Test))
worth_test_file.close()