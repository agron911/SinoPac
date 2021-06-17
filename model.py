import numpy as np
import pandas as pd
import csv
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from matplotlib import pyplot as plt
import matplotlib.font_manager

plt.rcParams['font.sans-serif']=['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus']=False


batch_size = 4
epochs = 50
time_step = 6 # 用6天來預測
input_size = 15  #預測天數
look_back = time_step * input_size
showdays = 300  #測試天數

X_train = []
y_train = []
X_validation = []
y_validation = []
testset = []  #保存測試基金淨值
forget_days = 5

def create_dataset(dataset):
    dataX, dataY = [], []
    print('len of dataset: {}'.format(len(dataset)))
    for i in range(0, len(dataset) - look_back, input_size):
        x = dataset[i: i + look_back]
        dataX.append(x)
        y = dataset[i + look_back: i + look_back + input_size]
        dataY.append(y)
    return np.array(dataX), np.array(dataY)

def build_model():
    model = Sequential()
    model.add(LSTM(units=128, input_shape=(time_step, input_size)))
    model.add(Dense(units=input_size))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


seed = 7
np.random.seed(seed)

fileTrain = './Train1.csv'
fileTest = './Test1.csv'

# 訓練及
with open(fileTrain) as f:
    row = csv.reader(f, delimiter=',')
    for r in row:
        dataset = []
        r = [x for x in r if x != 'None']  
        days = len(r) - 1 #兩天比較之漲跌幅
        if days <= look_back + input_size:  #忽略有效天數太少的
            continue
        for i in range(days):
            f1 = float(r[i])
            f2 = float(r[i+1])
            if f1 == 0 or f2 == 0:
                dataset = []
                break
            f2 = (f2 - f1) / f1 * 100
            if f2 > 15 or f2 < -15:  #漲跌幅超過15%，有可能有問題
                dataset = []
                break
            dataset.append(f2)
        n = len(dataset)
        n -= forget_days
        if n >= look_back + input_size:
            m = n % input_size
            X_1, y_1 = create_dataset(dataset[m:n])
            X_train = np.append(X_train, X_1)
            y_train = np.append(y_train, y_1)

#測試集
with open(fileTest) as f:
    row = csv.reader(f, delimiter=',')
    for r in row:
        dataset = []
        r = [x for x in r if x != 'None']
        days = len(r) - 1
        if days <= look_back:
            print('only {} days data. exit.'.format(days))
            continue
        if days > showdays:
            r = r[days-showdays:]
            days = len(r) - 1
        for i in range(days):
            f1 = float(r[i])
            f2 = float(r[i+1])
            if f1 == 0 or f2 == 0:
                print('zero value found. exit.')
                dataset = []
                break
            f2 = (f2 - f1) / f1 * 100
            if f2 > 15 or f2 < -15:
                print('{} greater then 15 percent. exit.'.format(f2))
                dataset = []
                break
            testset.append(f1)
            dataset.append(f2)
        f1=float(r[days])
        testset.append(f1)
        if forget_days < input_size:
            for i in range(forget_days,input_size):
                dataset.append(0)
                testset.append(np.nan)
        else:
            dataset = dataset[:len(dataset) - forget_days + input_size]
            testset = testset[:len(testset) - forget_days + input_size]
        if len(dataset) >= look_back + input_size:
            m = (len(testset) - 1) % input_size
            testset = testset[m:]
            m = len(dataset) % input_size
            X_validation, y_validation = create_dataset(dataset[m:])

#將輸入轉換成[樣本數，時間，特徵數]
X_train = X_train.reshape(-1, time_step, input_size)
X_validation = X_validation.reshape(-1, time_step, input_size)


#將輸出轉換成[樣本數，特徵數]
y_train = y_train.reshape(-1, input_size)
y_validation = y_validation.reshape(-1, input_size)

print('num of X_train: {}\tnum of y_train: {}'.format(len(X_train), len(y_train)))
print('num of X_validation: {}\tnum of y_validation: {}'.format(len(X_validation), len(y_validation)))

#訓練
model = build_model()
model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1, validation_split=0.25, shuffle=True)

#評估模型
train_score = model.evaluate(X_train, y_train, verbose=0)
validation_score = model.evaluate(X_validation, y_validation, verbose=0)

#預測
predict_validation = model.predict(X_validation)

if forget_days < input_size:
    for i in range(forget_days,input_size):
        y_validation[-1, i] = np.nan

print('Train Set Score: {:.3f}'.format(train_score))
print('Test Set Score: {:.3f}'.format(validation_score))
print('未來{}天實際漲幅：{}'.format(input_size, y_validation[-1]))
print('未來{}天預測漲幅：{}'.format(input_size, predict_validation[-1]))

y_validation = y_validation.reshape(-1, 1)
predict_validation = predict_validation.reshape(-1, 1)
testset = np.array(testset).reshape(-1, 1)

fig=plt.figure(figsize=(15,6))
plt.plot(y_validation, color='blue', label='每日基金')
plt.plot(predict_validation, color='red', label='預測每日')
plt.legend(loc='upper left')
plt.title('關聯組：{}組，預測天數：{}天，回退天數：{}天'.format(time_step, input_size, forget_days))
plt.show()


# 實際淨值，預測淨值
y_validation_plot = np.empty_like(testset)
predict_validation_plot = np.empty_like(testset)
y_validation_plot[:, :] = np.nan
predict_validation_plot[:, :] = np.nan

y = testset[look_back, 0]
p = testset[look_back, 0]
for i in range(look_back, len(testset)-1):
    y *= (1 + y_validation[i-look_back, 0] / 100)
    p *= (1 + predict_validation[i-look_back, 0] / 100)
    #print('{:.4f} {:.4f} {:.4f}'.format(testset[i+1,0], y, p))
    y_validation_plot[i, :] = y
    predict_validation_plot[i, :] = p


fig=plt.figure(figsize=(15,6))
plt.plot(y_validation_plot, color='blue', label='每日淨值')
plt.plot(predict_validation_plot, color='red', label='預測每日淨值')
plt.legend(loc='upper left')
plt.title('關聯組：{}組，預測天數：{}天，回退天數：{}天'.format(time_step, input_size, forget_days))
plt.show()