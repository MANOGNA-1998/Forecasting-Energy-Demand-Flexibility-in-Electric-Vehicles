#!/usr/bin/env python
# coding: utf-8

# In[172]:


import json
import pandas as pd


# In[173]:


file = open("acndata_sessions.json")
data = json.load(file)


# In[174]:


data.keys()


# In[175]:


data["_meta"]


# In[176]:


len(data["_items"])


# In[177]:


list(data["_items"][0].keys())


# In[178]:


df = pd.DataFrame(data["_items"])


# In[179]:


df.columns


# In[180]:


list(data["_items"][0].keys()) == list(df.columns)


# In[181]:


df.shape


# In[182]:


df.head()


# In[183]:


df.userID.nunique()


# In[184]:


noneList = list(df.head(1)["userInputs"])


# In[185]:


validUserInputIdxes = []
for index, row in df.iterrows():
    if (row["userInputs"] != None):
        validUserInputIdxes.append(index)
print(len(validUserInputIdxes))
    


# In[186]:


df.shape


# In[187]:


lens = {}
for index, row in df.iterrows():
    if (row["userInputs"] != None):
        lens[len(row['userInputs'])] = lens.get(len(row['userInputs']), 0) + 1


# In[188]:


lens


# ## There are mostly 1 or 2 user inputs. Must decide on this

# ## Working on times

# In[189]:


connTimes = list(df.connectionTime.values)


# In[190]:


dt = connTimes[0]
dt


# In[191]:


connTimes


# In[192]:


import datetime
timeStamp = datetime.datetime.strptime(dt, '%a, %d %b %Y %H:%M:%S %Z')
print(timeStamp)


# In[193]:


df["connectionTime"] = df["connectionTime"].apply(lambda dt : datetime.datetime.strptime(dt, '%a, %d %b %Y %H:%M:%S %Z'))


# In[194]:


df["connectionTime"]


# In[195]:


df["disconnectTime"]


# In[196]:


df["disconnectTime"] = df["disconnectTime"].apply(lambda dt : datetime.datetime.strptime(dt, '%a, %d %b %Y %H:%M:%S %Z'))


# In[197]:


df["disconnectTime"]


# In[198]:


df["doneChargingTime"]


# In[199]:


df["doneChargingTime"] = df["doneChargingTime"].apply(lambda dt : datetime.datetime.strptime(dt, '%a, %d %b %Y %H:%M:%S %Z') if dt else None)


# In[200]:


df["doneChargingTime"]


# In[201]:


df.head()


# In[202]:


print(df["disconnectTime"][0] - df["connectionTime"][0])


# In[203]:


(df["disconnectTime"][0] - df["connectionTime"][0]).total_seconds()


# In[204]:


totalConnectionTime = []
totalChargingTime = []
connectionTime = list(df.connectionTime)
disconnectTime = list(df.disconnectTime)
doneChargingTime = list(df.doneChargingTime)


# In[205]:


len(connectionTime) == len(disconnectTime) == len(doneChargingTime)


# In[206]:


for cT, dT in zip(connectionTime, disconnectTime):
    if cT and dT:
        totalConnectionTime.append((dT - cT).total_seconds())
    else:
        totalConnectionTime.append(None)


# In[207]:


len(connectionTime) == len(disconnectTime) == len(doneChargingTime) == len(totalConnectionTime)


# In[208]:


totalConnectionTime


# In[209]:


for cT, dCt in zip(connectionTime, doneChargingTime):
    if cT and dCt:
        totalChargingTime.append((dCt - cT).total_seconds())
    else:
        totalChargingTime.append(None)


# In[210]:


len(connectionTime) == len(disconnectTime) == len(doneChargingTime) == len(totalConnectionTime) == len(totalChargingTime)


# In[211]:


totalChargingTime


# In[212]:


df["totalChargingTime"] = totalChargingTime


# In[213]:


df["totalConnectionTime"] = totalConnectionTime


# In[214]:


df


# ## ClusterId

# In[215]:


df.clusterID.value_counts()


# ## All values are same. Dropping the column

# In[216]:


df.drop(columns = ["clusterID"], inplace = True)


# In[217]:


df.head()


# ## Some EDA

# In[218]:


corr = df.corr("spearman")


# In[219]:


import seaborn as sns


# In[220]:


cmap = cmap=sns.diverging_palette(5, 250, as_cmap=True)

def magnify():
    return [dict(selector="th",
                 props=[("font-size", "7pt")]),
            dict(selector="td",
                 props=[('padding', "0em 0em")]),
            dict(selector="th:hover",
                 props=[("font-size", "12pt")]),
            dict(selector="tr:hover td:hover",
                 props=[('max-width', '200px'),
                        ('font-size', '12pt')])
]

corr.style.background_gradient(cmap, axis=1)    .set_properties(**{'max-width': '80px', 'font-size': '10pt'})    .set_precision(2)    .set_table_styles(magnify())


# ## Plotting correlation

# In[221]:


import seaborn as sns


# In[222]:


sns.heatmap(corr, 
        xticklabels=corr.columns,
        yticklabels=corr.columns)


# In[223]:


df.head()


# In[224]:


hist = (df["totalConnectionTime"] - df["totalChargingTime"]).hist(bins=50)


# In[225]:


meterValues.shape


# In[226]:


(df["totalConnectionTime"]/(60*60) - df["totalChargingTime"]/(60*60)).hist(bins = 50)


# In[227]:


extraTime = pd.DataFrame()


# In[228]:


extraTime["time"] = df["totalConnectionTime"]/(60*60) - df["totalChargingTime"]/(60*60)


# In[229]:


extraTime


# In[230]:


print(extraTime.boxplot(column=['time']))


# In[231]:


df.to_csv("caltech.csv")


# # ElaadNL
# ## Quantifying flexibility

# ### MeterValues

# In[2]:


import pandas as pd


# In[3]:


meterValues = pd.read_excel("open_metervalues.xlsx")


# In[4]:


meterValues.shape


# In[5]:


meterValues.columns


# In[6]:


meterValues.dtypes


# In[8]:


import seaborn as sns


# In[9]:


cmap = cmap=sns.diverging_palette(5, 250, as_cmap=True)

def magnify():
    return [dict(selector="th",
                 props=[("font-size", "7pt")]),
            dict(selector="td",
                 props=[('padding', "0em 0em")]),
            dict(selector="th:hover",
                 props=[("font-size", "12pt")]),
            dict(selector="tr:hover td:hover",
                 props=[('max-width', '200px'),
                        ('font-size', '12pt')])
]

meterValues.corr("pearson").style.background_gradient(cmap, axis=1)    .set_properties(**{'max-width': '80px', 'font-size': '10pt'})    .set_precision(2)    .set_table_styles(magnify())


# In[237]:


sns.heatmap(meterValues.corr(), 
        xticklabels=meterValues.corr().columns,
        yticklabels=meterValues.corr().columns)


# In[238]:


meterValues.head()


# Transaction IDThe unique transaction code. 
#  
# ChargePoint IDThe unique code of a charging station
# 
# Connector IDMany charging stations have two connections (two sockets for charge plugs) and this indicates what connector was used for the transactions.
# 
# UTCTimeDate and timestamp of the metervalue. 
# 
# Collectedvalue Metervalue in kWh per datetime.
# 
# EnergyInterval
# Total energy (kWh) transfer between two consecutive meter readings. 
# 
# AveragePowerAverage power in kW between two consecutive meter readings. 
# 

# In[239]:


transactions.head()


# In[240]:


meterValues.TransactionId.nunique()


# In[241]:


meterValues.shape


# In[242]:


pd.options.display.max_seq_items = 20


# In[243]:


meterValues.TransactionId.value_counts()


# In[244]:


meterValues[meterValues["TransactionId"] == 3570919]


# In[245]:


meterValues.to_csv("metervalues.csv")


# ### Transactions

# In[10]:


transactions = pd.read_excel("open_transactions.xlsx")


# In[11]:


transactions


# In[12]:


set(transactions.TransactionId) == set(meterValues.TransactionId)


# <b>Transaction</b> ID The unique transaction code. 
# 
# ChargePoint IDThe unique code of a charging station. 
# 
# Connector IDMany charging stations have two connections (two sockets for charge plugs) and this indicates what connector was used for the transactions.
# 
# UTCTransactionStartThe moment the transaction was started (logged in locale time zone). 
# 
# UTCTransactionStop The moment the plug was disconnected and the transaction was stopped.
# 
# StartCard
# The RFID card (hashed) which has been used to start a transaction.
# 
# ConnectedTime
# Time difference between the start and end of a transaction. 
#  
# ChargeTime
# Total time wherein energy transfer took place. 
#  
# TotalEnergy 
# The total energy demand (kWh) per session.
#  
# MaxPower
# The maximum charging rate (kW) during a session.
# 

# In[13]:


cmap = cmap=sns.diverging_palette(5, 250, as_cmap=True)

transactions.corr("pearson").style.background_gradient(cmap, axis=1)    .set_properties(**{'max-width': '80px', 'font-size': '10pt'})    .set_precision(2)    .set_table_styles(magnify())


# In[14]:


transactions.to_csv("transactions.csv")


# In[15]:


transactions.head()


# ## Finding connection start times. So that we can find what times are most in demand

# In[16]:


startTime = transactions.UTCTransactionStart[0]


# In[17]:


print(startTime.time())


# In[18]:


startTimes = [i for i in transactions.UTCTransactionStart]
startHours = []
startMinutes = []


# In[19]:


startTimes[0].time().hour


# In[20]:


for idx in range(len(startTimes)):
    startTimes[idx] = startTimes[idx].time()
    startHours.append(startTimes[idx].hour)
    startMinutes.append(startTimes[idx].minute)
    


# In[21]:


startTimes


# In[22]:


transactions["StartHour"] = startHours
transactions["StartMinutes"] = startMinutes


# In[23]:


transactions["StartTime"] = startTimes


# In[24]:


transactions.head()


# In[25]:


startTimes[0]


# In[26]:


#transactions.resample('H', on='StartTime').TransactionId.count()


# In[29]:


import matplotlib.pyplot as plt
import matplotlib


# In[30]:


ax = transactions.hist(column='StartHour', bins = 24,grid=False, figsize=(20,12), color='#86bf91', zorder=2, rwidth=0.9)
ax = ax[0]
for x in ax:

    # Despine
    x.spines['right'].set_visible(False)
    x.spines['top'].set_visible(False)
    x.spines['left'].set_visible(False)

    # Switch off ticks
    x.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

    # Draw horizontal axis lines
    vals = x.get_yticks()
    for tick in vals:
        x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

    # Remove title
    x.set_title("")

    # Set x-axis label
    x.set_xlabel("Start Hours", labelpad=20, weight='bold', size=12)

    # Set y-axis label
    x.set_ylabel("No. of Sessions", labelpad=20, weight='bold', size=12)

    # Format y-axis label
    x.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,g}'))


# In[31]:



import plotly.express as px
  
fig = px.histogram(transactions, x="StartHour", marginal = 'box')
fig.show()


# ## Observations
# q1 = 09 Hrs,
# Median = 12 Hrs,
# q3 = 16Hrs
# 

# In[32]:


transactions.plot.scatter(x = "StartHour", y = "ChargeTime")


# In[34]:


ax = transactions.hist(column='ChargeTime', bins = 24,grid=False, figsize=(20,12), color='#86bf91', zorder=2, rwidth=0.9)
ax = ax[0]
for x in ax:

    # Despine
    x.spines['right'].set_visible(False)
    x.spines['top'].set_visible(False)
    x.spines['left'].set_visible(False)

    # Switch off ticks
    x.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

    # Draw horizontal axis lines
    vals = x.get_yticks()
    for tick in vals:
        x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

    # Remove title
    x.set_title("")

    # Set x-axis label
    x.set_xlabel("Charge Time(Hrs)", labelpad=20, weight='bold', size=12)

    # Set y-axis label
    x.set_ylabel("No. of Sessions", labelpad=20, weight='bold', size=12)

    # Format y-axis label
    x.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,g}'))


# In[36]:


fig = px.histogram(transactions, x="ChargeTime", marginal = 'box')
fig.show()


# ## Observations
# ### Min: 0.02
# ### q1: 1.25
# ### median: 2.24
# ### q3: 3.5
# ### Upper fence: 6.87

# In[57]:


fig = px.histogram(transactions, x="TotalEnergy", marginal = 'box')
fig.show()


# In[ ]:





# In[37]:


transactions


# In[38]:


extraTime


# In[39]:


max(list(extraTime.time))


# In[40]:


print(extraTime.boxplot("time"))


# In[41]:


fig = px.histogram(extraTime, x="time", marginal = 'box')
fig.show()


# In[42]:


df.head()


# In[43]:


df.iloc[222].userInputs


# In[44]:


meterValues.head()


# In[45]:


transactions[transactions["ChargePoint"] == "5ab468315a1f42feb6d0a87307593352"]


# In[58]:


len(set(transactions.ChargePoint))


# In[59]:


crossDf = transactions[["StartHour", "ChargeTime"]]


# In[60]:


sns.heatmap(crossDf, vmin=0, vmax=40)
plt.show()


# In[61]:


meterValues.head()


# In[50]:


meterValues.to_csv("metervaluesPostCleaning.csv")


# In[51]:


transactions.to_csv("transactionPostCleaning.csv")


# In[52]:


df.to_csv("caltechPostCleaning.csv")


# In[53]:


df.head()


# In[63]:


transactions.head()


# In[67]:


extraTimes = pd.DataFrame({"ExtraTime" : list(transactions["ConnectedTime"] - transactions["ChargeTime"]) } )


# In[68]:


fig = px.histogram(extraTimes, x="ExtraTime", marginal = 'box')
fig.show()


# In[ ]:




