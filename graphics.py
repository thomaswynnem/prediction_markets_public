## Graphing Data for Visualization

## All Contracts Visualization First

import seaborn as sns 
import matplotlib.pyplot as plt 
import pandas as pd
import ast


## Plot for Avg Spending on Each Category
data = pd.read_csv("data/silver/allContracts/CategorySpending.csv")

adjusted = data.melt(var_name='categories', value_name='amounts')

print(adjusted)

sns.barplot(x='categories',y='amounts', data=adjusted)
plt.show()

## Plot for Yes vs No Outcome Markets

data = pd.read_csv("data/silver/allContracts/contractSplits.csv")

data = data.loc[:,data.columns != 'averageSpend']

adjusted = data.melt(var_name='outcome', value_name='amounts')

adjusted = adjusted[adjusted['outcome'] != 'Unnamed: 0']

adjusted.groupby(['outcome']).sum().plot(kind='pie', y='amounts')

plt.show()

## Rate of Correctness for Markets Based on Fund Distribution
'''
data = pd.read_csv("data/silver/allContracts/correctsRates.csv")

data = data.loc[:,data.columns != 'BettorCorrectRate']
data = data.loc[:,data.columns != 'contractCorrectRate']


print(cCRbyDistr)
print(Distribution)

print(adjusted)

sns.histplot(data=adjusted, x = 'Distribution', y = 'cCRbyDistr')

plt.show()

'''

## Correct Rate for Value of Bet

data = pd.read_csv("data/silver/allContracts/dollarly_valueDF.csv")

data = data.loc[:,data.columns != 'Unnamed: 0']

data = data.iloc[[1]]

data = data.reset_index(drop=True)

data = data.melt(var_name='bet values', value_name='correct rate')


print(data)

sns.barplot(data=data, x = 'bet values', y = 'correct rate')

plt.yticks([0,.05,.10,.15,.20,.25,.30,.35,.40,.45,.50,.55,.60,.65,.70,.75,.80])

plt.show()

## Correct Rate for Time of Bet

data = pd.read_csv("data/silver/allContracts/timeline_quarterDF.csv")

data = data.loc[:,data.columns != 'Unnamed: 0']

data = data.iloc[[2]]

ata = data.reset_index(drop=True)

data = data.melt(var_name='bet time', value_name='correct rate')

sns.barplot(data=data, x = 'bet time', y = 'correct rate')

plt.yticks([0,.05,.10,.15,.20,.25,.30,.35,.40,.45,.50,.55,.60,.65,.70,.75,.80,.85,.9,.95,1.0])

plt.show()

## Correct Rate for Time of Big Bet (Over 1000)

data = pd.read_csv("data/silver/allContracts/timeline_quarterDF.csv")

data = data.loc[:,data.columns != 'Unnamed: 0']

data = data.iloc[[4]]

ata = data.reset_index(drop=True)

data = data.melt(var_name='bet time', value_name='correct rate')

sns.barplot(data=data, x = 'bet time', y = 'correct rate')

plt.yticks([0,.05,.10,.15,.20,.25,.30,.35,.40,.45,.50,.55,.60,.65,.70,.75,.80,.85,.9,.95,1.0])

plt.show()

