# the purpose of this code is to go through the historical data
# of a market and extract price data as a function of time
# betfair historical data is stored in a data folder structure
# e.g. Month/Day/someRefNum/marketNumber.bz2
# extracting the required .bz2 archive produces a .json file and reads it

import numpy as np
import json

# open market data of associated match
mktData = []
#Use data from Liverpool vs Norwich game 9/8/19
fileStr = './19-08/BASIC/2019/Aug/9/29326095/1-159690672.JSON' 
with open(fileStr) as jsonFile:
    strList = jsonFile.readlines()
    for obj in strList:
        data = json.loads(obj)
        mktData.append(data)
#get ID numbers for runners
runners = mktData[0]['mc'][0]['marketDefinition']['runners']
idList = []
for idNum in runners:
    idList.append(idNum['id'])

#create list for runners
ID1 = idList[0]
ID1price = [np.nan]
ID2 = idList[1]
ID2price = [np.nan]
ID3 = idList[2]
ID3price = [np.nan]
t = [mktData[0]['pt']]
# loop through data updating prices at each update
timestampEnd = 1000*match['extractTime'].timestamp()
curTimestamp = 0
for element in mktData[1:]:
    curTimestamp = element['pt']
    if curTimestamp <= timestampEnd:
        t.append(element['pt'])
        #copy previous price
        ID1price.append(ID1price[-1])
        ID2price.append(ID2price[-1])
        ID3price.append(ID3price[-1])
        try:
            for price in element['mc'][0]['rc']:
                #overwrite price if update
                if price['id'] == ID1:
                    ID1price[-1] = price['ltp']
                elif price['id'] == ID2:
                    ID2price[-1] = price['ltp']
                elif price['id'] == ID3:
                    ID3price[-1] = price['ltp']
        except:
            error = 1
            #print('Failed at ', element['clk'])
match['homeExtract'] = ID1price[-1]
match['awayExtract'] = ID2price[-1]
match['drawExtract'] = ID3price[-1]

timeOff = np.ones(len(t))*float(t[0])
time = np.array(t)
time = (time.astype(np.float) - timeOff)/60000/1440

home = np.array(ID1price)
draw = np.array(ID2price)
away = np.array(ID3price)

import datetime as dt
time2 = np.array(t)
time2 = time2.astype(np.float)
print(dt.datetime.fromtimestamp(time2[0]/1000))
print(dt.datetime.fromtimestamp(time2[-1]/1000))


import matplotlib.pyplot as plt
Phome = np.reciprocal(ID1price)
Pdraw = np.reciprocal(ID2price)
Paway = np.reciprocal(ID3price)
plt.plot(time, Phome,
        time, Pdraw,
        time, Paway)
plt.legend([runners[0]['name'], runners[1]['name'], runners[2]['name']])
plt.xlabel('Time (days)')
plt.ylabel('Probability')
plt.show()
