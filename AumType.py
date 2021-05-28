from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import time
# df = pd.read_csv('架上基金一覽表_20210331.csv',index_col="基金代號")
df = pd.read_csv('架上基金一覽表_20210331.csv')
print(df.shape)
print(matplotlib.matplotlib_fname()) 

# 按照基金類型分類
print(matplotlib.__file__)
groupcnt=df.groupby('AUM類別').agg(fundcnt=('AUM類別','count')).\
sort_values(by='fundcnt',ascending=False).reset_index('AUM類別')

fig=plt.figure(figsize=(20,8))
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.bar(x='AUM類別',height='fundcnt',data=groupcnt)
for a,b in zip(range(len(groupcnt.index)),groupcnt.fundcnt):
    plt.text(a,b,b,ha='center',va='bottom',fontsize=16)
plt.title('各類基金',fontdict={'fontsize':20})
plt.show()
