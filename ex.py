import pandas as pd
import requests
import time
import execjs
# import os
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']='SimHei'
plt.rcParams['axes.unicode_minus']=False

url = 'http://fund.eastmoney.com/js/fundcode_search.js'
content = requests.get(url)
jsContent = execjs.compile(content.text)
rawData = jsContent.eval('r')

codes=[]
codeHHC = [] 
names=[]
type=[]

for code in rawData:
    if len(code) > 2:
        codes.append(code[0])
        names.append(code[2])
        type.append(code[3])
        
        name = code[2]
        if code[3] == '混合型' and name[-1] == 'C':
            codeHHC.append(code[0])

info=pd.DataFrame({'代碼':codes, '名稱':names, '類型':type})

info.to_csv('code.csv', encoding='utf_8_sig', index=False)

# print(jjinfo)
def getUrl(fscode):
    head = 'http://fund.eastmoney.com/pingzhongdata/'
    tail = '.js?v='+ time.strftime("%Y%m%d%H%M%S",time.localtime())
    return head+fscode+tail

# 抓淨值
def getWorth(fscode):
    content = requests.get(getUrl(fscode))
    jsContent = execjs.compile(content.text)
    name = jsContent.eval('fS_name')
    code = jsContent.eval('fS_code')
    
    net_trend = jsContent.eval('Data_netWorthTrend')
    
    ac_trend = jsContent.eval('Data_ACWorthTrend')
    netWorth = []
    ACWorth = []
    for dayWorth in net_trend[::-1]:
        netWorth.append(dayWorth['y'])
    for dayACWorth in ac_trend[::-1]:
        ACWorth.append(dayACWorth[1])
    return netWorth, ACWorth

net_file = open('netHHC.csv','w')
ac_file = open('accHHC.csv','w')

i = 0
j = len(codeHHC)
for code in codeHHC:
    i += 1
    try:
        net_Worth, AC_Worth = getWorth(code)
    except:
        continue
    if len(net_Worth) <= 0 or len(AC_Worth) < 0:
        continue
    net_file.write("\'"+code+"\',")
    net_file.write(",".join(list(map(str, net_Worth))))
    net_file.write("\n")
    ac_file.write("\'"+code+"\',")
    ac_file.write(",".join(list(map(str, AC_Worth))))
    ac_file.write("\n")
    if i % 50 == 0:
        print("total : {}\t process : {}".format(j, i))
print(net_file.close())
print(ac_file.close())
