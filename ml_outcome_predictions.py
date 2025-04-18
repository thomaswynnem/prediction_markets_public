#!/usr/bin/env python
# coding: utf-8

# ## Predicting Market Outcomes: Utilizes Data Research and DataFrames to Cluster Data
# 
# Utilized Traits:
# * Betting Data (Investment Amounts, Frequency, Wallets)
# * Outcome Data (Distribution, Winner)
# * Market Details (Category, Date, Time Length)

# Open DataFrames

# In[21]:


import pandas as pd

marketOutcomes = pd.read_csv('data/silver/marketOutcomes.csv')
markets = pd.read_csv('data/silver/markets_with_ai_categories.csv')


# Obtain Addresses

# In[22]:


addresses = markets['marketMakerAddress']


# In[23]:


import os
from dotenv import load_dotenv
import requests
import pprint
import pandas as pd
load_dotenv()
from datetime import datetime, timedelta
POLYGON_API_KEY = os.getenv("POLYGONSCAN_API_KEY")
print(POLYGON_API_KEY)
def time_decoder(address: str, iter: int = None, sz: str = None, hundredPlusBuys = None, lessThanHundredBuys = None): 
    dictForAddys = {}
    if sz is not None:
        if sz == 'large':
            dictForAddys = hundredPlusBuys[iter]
        elif sz == 'small':
            dictForAddys = lessThanHundredBuys[iter]
    
    else:
        try:
            dictForAddys = pd.read_csv(f'data/bronze/contract_buy_{address}.csv')
        except FileNotFoundError:
            return None
    try:
        
        people = [addy for addy in dictForAddys['buyer']]  
        people = [a.lower() for a in people]
        
    except KeyError:
        return None
    url = (
      f'https://api.polygonscan.com/api'
      f'?module=account'
      f'&action=tokentx'
      f'&address={address}'
      f'&startblock=0'
      f'&endblock=99999999'
      f'&apikey={POLYGON_API_KEY}'
    )
    response = requests.get(url)


    transactionDict = response.json()
    status = transactionDict.get("status")
    if status != '1':
        print(f"Error: {transactionDict.get('message')}")
        return None


    timeDict = {}
    for row in transactionDict.get('result', []):
      
      if row.get('from', '').lower() in people:
            try:
               timeDict[row.get('from','').lower()].append(row.get('timeStamp'))
            except KeyError:
               timeDict[row.get('from', '').lower()] = [row.get('timeStamp')]

    from datetime import datetime
    allTimes = [ts for ts_list in timeDict.values() for ts in ts_list]

    
    minTimestamp = min(datetime.fromtimestamp(int(x)) for x in allTimes)
    for buyer, lst in timeDict.items():
        lst_dt = sorted(datetime.fromtimestamp(int(x)) for x in lst)
        timeDict[buyer] = [
            int((ts - minTimestamp).total_seconds())   
            for ts in lst_dt
        ]
    
    buyers= dictForAddys['buyer'].str.lower()
    dictForAddys['timeStampSinceFirst'] = [timeDict[addy].pop(0) if addy in timeDict and timeDict[addy] else None for addy in buyers]
    dictForAddys.drop('timeStamp', axis=1, inplace=True)
    dictForAddys.to_csv(f'data/bronze/contract_official_buys_{address}.csv')

    return timeDict


# In[24]:


timerStamper = []
turn = 0
for index, market in markets.iterrows():
    turn += 1
    print(f"Turn {turn} of {len(markets)}")
    try:
        timeStamp  = time_decoder(market["marketMakerAddress"])
    except:
        continue    
    print("Yahoo News")
    try:
        buyScans = pd.read_csv(f'data/bronze/contract_official_buys_{market["marketMakerAddress"]}.csv')
    except FileNotFoundError:
        print(f"Error: 1")
        continue
    try:
        buyScans75Index = max(buyScans['timeStampSinceFirst'].tolist())*.50
        buyScans75 = buyScans[buyScans['timeStampSinceFirst'] < buyScans75Index]
        
    except:
        print(f"Error: Unicorn")
        continue
    try:
        filtered = marketOutcomes.loc[marketOutcomes["marketMakerAddress"] == market["marketMakerAddress"], "index"]
        marketOutcomeIndex = filtered.iloc[0]
    except:
        print(f"Error: 2")
        continue
    
    try:
        buysIndex0 = buyScans75[buyScans75['outcomeIndex'] == 0]['investmentAmount']
        buysIndex1 = buyScans75[buyScans75['outcomeIndex'] == 1]['investmentAmount']
    except:
        print(f"Error: 3")
        continue
    
    try:
        total = sum(buyScans75['investmentAmount'].tolist())
        bigBets = buyScans75[buyScans75['investmentAmount'] > .05*total]
        buyScansVC = bigBets['outcomeIndex'].value_counts()
        whale0 = buyScansVC.get(0, 0)
        whale1 = buyScansVC.get(1, 0)
    except:
        print("Error: 5")
        continue
    
    try: 
        sz = len(buyScans75)
        finalRatioVC = buyScans75['outcomeIndex'].value_counts()
        count0 = finalRatioVC.get(0, 0)
        count1 = finalRatioVC.get(1, 0)
        ratio = count0 / (count0 + count1)
    except:
        print("Error: 6")
        continue
        
    try:
        timerStamper.append({'Market': market['marketMakerAddress'], 'Category': market['category'], 'TimeStamps': timeStamp, 'BuysIndex0': buysIndex0.tolist(), 'BuysIndex1': buysIndex1.tolist(), 'OutcomeIndex': marketOutcomeIndex, 'Whale0': whale0, 'Whale1': whale1, 'FinalRatio': ratio})
        print("Added")
    except:
        print("Timer Failure")
        
    print("Success")
timerStamper = pd.DataFrame(timerStamper)
timerStamper.to_csv('data/silver/timerStamper2.csv', index=False)


# Creating Official ML Model Training Data

# In[ ]:


import pandas as pd
timerStamper = pd.read_csv("data/silver/timerStamper2.csv")

from sklearn.preprocessing import LabelEncoder
badIndeces = []
encoder = LabelEncoder()
timerStamper['CategoryEncoded'] = encoder.fit_transform(timerStamper['Category'])
from datetime import timedelta
import ast
dataSector = []
for iter, line in timerStamper.iterrows():
    buysIndex0 = ast.literal_eval(line['BuysIndex0'])
    buysIndex1 = ast.literal_eval(line['BuysIndex1'])
    try:
        timeDict = ast.literal_eval(line['TimeStamps'])
        allDeltas = []
        for deltas in timeDict.values():
            allDeltas.extend(deltas)
        maxDelta = max(allDeltas)
    except:
        badIndeces.append(iter)
        print("Error: 7")
        continue
    # Total length of time of the market
    if None in [line['CategoryEncoded'], maxDelta , sum(buysIndex0), sum(buysIndex1), line['Whale0'], line['Whale1'], line['FinalRatio']] or (len(buysIndex0) + len(buysIndex1)) < 10:
        badIndeces.append(iter)
        continue
    dataSector.append([[line['CategoryEncoded'], maxDelta ,len(buysIndex0), sum(buysIndex0), len(buysIndex1), sum(buysIndex1), line['Whale0'], line['Whale1'], line['FinalRatio']], line['OutcomeIndex']])
    print(line['OutcomeIndex'])
    
timerStamper.drop(badIndeces, inplace=True)
timerStamper.reset_index(drop=True, inplace=True)
timerStamper.to_csv('data/silver/timerStamper2.csv', index=False)


# Splitting Data into Test and Train

# In[ ]:


import torch

import torch
from torch.utils.data import Dataset, DataLoader

class BinaryDataset(Dataset):
    def __init__(self, features, labels):
        self.features = torch.tensor(features, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.float32) # Use float for binary labels
        
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]


totalData = len(dataSector)

trainCap = totalData*4 // 5

trainDataInputs = [x[0] for x in dataSector[:trainCap]]
trainResults = [x[1] for x in dataSector[:trainCap]]

testDataInputs = [x[0] for x in dataSector[trainCap:]]
testResults = [x[1] for x in dataSector[trainCap:]]

from sklearn.preprocessing import StandardScaler
import numpy as np


X_train = np.array(trainDataInputs)
X_test = np.array(testDataInputs)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(trainResults, dtype=torch.float32)
y_test_tensor = torch.tensor(testResults, dtype=torch.float32)

trainData = BinaryDataset(X_train_tensor, y_train_tensor)
testData = BinaryDataset(X_test_tensor, y_test_tensor)

batch_size = 10
shuffle = True
dataLoader = DataLoader(trainData, batch_size=batch_size, shuffle=shuffle)
dataLoaderTest = DataLoader(testData, batch_size=batch_size, shuffle=shuffle)




# Creating the Model

# Model Architecture taken from here : https://medium.com/data-science/pytorch-tabular-binary-classification-a0368da5bb89
# 
# Key Point: Relu serves to fid complex relationships between variables
# Key Point: Normalizing to keep everything within 0 to 1 scope and not put too much weight on anything
# Key Point: Linear Layers Attempt to make reason out of data

# In[ ]:


import torch
import torch.nn as nn
class MarketPredictor(nn.Module):
    "Initializes multi-class classification model"
    def __init__(self, input_features=9, output_features=1, hidden_units=16):
        super().__init__()
        self.layer_1 = nn.Linear(input_features, hidden_units) 
        self.layer_2 = nn.Linear(hidden_units, hidden_units)
        self.layer_out = nn.Linear(hidden_units, output_features) 
        
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.1)
        self.batchnorm1 = nn.BatchNorm1d(hidden_units)
        self.batchnorm2 = nn.BatchNorm1d(hidden_units)
        
    def forward(self, inputs):
        x = self.relu(self.layer_1(inputs))
        x = self.batchnorm1(x)
        x = self.relu(self.layer_2(x))
        x = self.batchnorm2(x)
        x = self.dropout(x)
        x = self.layer_out(x)
        
        return x

MarketPredictorModel = MarketPredictor(input_features=9,
                    output_features=1,
                    hidden_units=16)


class MarketPredictorLinear(nn.Module):
    "Simplified linear model for binary classification"
    def __init__(self, input_features=9, output_features=1, hidden_units = 8):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_features, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units,output_features),
        )
        

    def forward(self, x):
        return self.model(x)

MarketPredictorLinearModel = MarketPredictorLinear(input_features=9,
                    output_features=1,
                    hidden_units = 8)
lossFn = nn.BCEWithLogitsLoss()
optimizerReg = torch.optim.Adam(MarketPredictorModel.parameters(), lr=0.001)
optimizerLin = torch.optim.Adam(MarketPredictorLinearModel.parameters(), lr=0.001)


# A way to Analyze Accuracy (Literally just a percent)

# In[ ]:


def binaryAccuracy(actualOutcomes, predProbs, threshold=0.5):
    preds = (predProbs > threshold).float()
    correct = (preds == actualOutcomes).float().sum()
    acc = correct / actualOutcomes.shape[0]
    return acc * 100


# Training Data

# Both training and testing

# In[ ]:


import random

'''
def train(epochs: int):
  rates = []
  maxAcc = 0
  for epoch in range(epochs):
    MarketPredictorModel.train()
    trainIndex = random.randint(736)
    binaryPredictions = MarketPredictorModel(trainData[trainIndex]).squeeze()
    loss = lossFn(binaryPredictions, trainResults)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    probs1 = torch.sigmoid(binaryPredictions)
    accuracy = binaryAccuracy(trainResults, probs1)
    MarketPredictorModel.eval()
    
    with torch.inference_mode():
      indexTest = random.randint(100)
      testPredictions = MarketPredictorModel(testData[indexTest]).squeeze()
      lossTest = lossFn(testPredictions, testResults[indexTest])
      probs = torch.sigmoid(testPredictions)
      accTest = binaryAccuracy(testResults, probs)
      
      
      print(f"Epoch: {epoch} | Loss: {loss:.5f} | Acc: {accuracy:.2f}% | Test Loss: {lossTest:.5f} | Test Acc: {accTest:.4f}")
      maxAcc = max(maxAcc, accTest)
      rates.append(accTest)
      
  import statistics
  return maxAcc, statistics.mean([r.item() for r in rates])
'''


import statistics as stat
def train_one_epoch(epoch_index, model, optimizer):
    model.train()
    running_loss = 0.
    last_loss = 0.


    for i, data in enumerate(dataLoader):
        # Every data instance is an input + label pair
        inputs, labels = data

        # Zero your gradients for every batch!
        optimizer.zero_grad()

        # Make predictions for this batch
        outputs = model(inputs)
        outputs = outputs.squeeze()
        loss = lossFn(outputs, labels)
        loss.backward()

        # Adjust learning weights
        optimizer.step()

        # Gather data and report
        running_loss += loss.item()
        outputsSig = torch.sigmoid(outputs)

        
def evaluate_full_test_set(test_loader, model):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs).squeeze()
            preds = torch.sigmoid(outputs)
            mask = (preds >= 0.6) | (preds <= 0.4)
            preds = preds[mask]
            labels = labels[mask]

            if len(preds) == 0:
                continue

            preds = preds > 0.5
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    return 100 * correct / total
        
        


# Training Data to be 85% accuracte

# In[ ]:


maxAcc = 0
mean = 0
epochs =50

for epoch in range(epochs):
    print(f"Epoch {epoch} of {epochs}")
    train_one_epoch(epoch, MarketPredictorModel, optimizerReg)
    avg  =evaluate_full_test_set(dataLoaderTest, MarketPredictorModel)
    print(f"Epoch {epoch} Accuracy: {avg}")
    
torch.save(MarketPredictorModel.state_dict(), "MarketPredictor.pt")


# In[ ]:


maxAcc = 0
mean = 0
epochs =250

for epoch in range(epochs):
    print(f"Epoch {epoch} of {epochs}")
    train_one_epoch(epoch,MarketPredictorLinearModel, optimizerLin)
    avg  =evaluate_full_test_set(dataLoaderTest, MarketPredictorLinearModel)
    print(f"Epoch {epoch} Accuracy: {avg}")
    
torch.save(MarketPredictorLinearModel.state_dict(), "MarketPredictorLinear.pt")


# maxAcc = 0
# mean = 0
# epochs =200
# 
# for epoch in range(epochs):
#     print(f"Epoch {epoch} of {epochs}")
#     train_one_epoch(epoch, None)
#     avg  =evaluate_full_test_set(dataLoaderTest)
#     print(f"Epoch {epoch} Accuracy: {avg}")
#     
# torch.save(MarketPredictorLinearModel.state_dict(), "MarketPredictor.pt")

# Analyzing Parameters

# In[ ]:


for name, param in MarketPredictorModel.named_parameters():
    if param.requires_grad:
        print(f"Layer: {name} | Shape: {param.shape}")
        print(param.data)
        print("-" * 40)


# In[ ]:


timerStamper = pd.read_csv("data/silver/timerStamper1.csv")

correct = 0
total  =0

for market in timerStamper['Market'].tolist():
    try:
        buyScans = pd.read_csv(f'data/bronze/contract_official_buys_{market}.csv')
    except FileNotFoundError:
        print(f"Error: 1")
        continue

    buyScans75Index = max(buyScans['timeStampSinceFirst'].tolist())*.50
    buyScans75 = buyScans[buyScans['timeStampSinceFirst'] < buyScans75Index]


    buysIndex0 = buyScans75[buyScans75['outcomeIndex'] == 0]['investmentAmount']
    buysIndex1 = buyScans75[buyScans75['outcomeIndex'] == 1]['investmentAmount']

    
    prediction = sum(buysIndex0)/(sum(buysIndex0) + sum(buysIndex1))
    if prediction > .4 and prediction < .6:
        continue
    prediction = 0 if prediction >= 0.5 else 1
    outcomeIndex = timerStamper[timerStamper['Market'] == market]['OutcomeIndex'].tolist()[0]
    
    if prediction == outcomeIndex:
        correct += 1
    total += 1
    
    
print(f"Correct: {correct} | Total: {total} | Accuracy: {correct/total*100}%")
    
    
    


# In[ ]:


# Assuming your model is called `MarketPredictorLinearModel`
input_layer_weights = MarketPredictorLinearModel.model[0].weight.detach().numpy()

# Shape: [hidden_units, input_features]
print("Weight matrix shape:", input_layer_weights.shape)

import numpy as np

feature_influence = np.mean(np.abs(input_layer_weights), axis=0)

for i, influence in enumerate(feature_influence):
    print(f"Feature {i}: Importance Score = {influence:.4f}")

