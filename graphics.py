## Graphing Data for Visualization

## All Contracts Visualization First

import seaborn as sns 
import matplotlib.pyplot as plt 
import pandas as pd
import ast
import numpy as np

###################################################################################################

### Plots for Total Market Data

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
# manually chaned dollarly_valueDF to have ints instead of intervals
print(data)

data = data.loc[:,data.columns != 'Unnamed: 0']

data = data.iloc[[1]]

data = data.melt(var_name='dollarly_value', value_name='correct_rate')

data = data.dropna()

print(data)

data['dollarly_value'] = data['dollarly_value'].astype(int) + 100


sns.scatterplot(x='dollarly_value',y='correct_rate', data=data, hue = 'dollarly_value',palette=['red', 'green', 'blue', 'yellow', 'cyan', 'purple', 'orange', 'pink', 'brown', 'black', 'grey'])





plt.show()


## Correct Rate for Time of Bet

data = pd.read_csv("data/silver/allContracts/timeline_quarterDF.csv")

data = data.loc[:,data.columns != 'Unnamed: 0']

data = data.iloc[[1,2]]

newdata = {'bet_time' : ['Q1','Q2','Q3','Q4'], 'correct_amounts': data.iloc[0]*data.iloc[1].values, 'incorrect_amounts': data.iloc[0] - (data.iloc[0]*data.iloc[1]).values}
newdata = pd.DataFrame(newdata) 
print(newdata)
pivot_data = newdata.set_index('bet_time').T
sns.heatmap(data = pivot_data, annot=True, fmt="g", cmap='viridis')


plt.show()

## Correct Rate for Time of Big Bet (Over 1000)

data = pd.read_csv("data/silver/allContracts/timeline_quarterDF.csv")

data = data.loc[:,data.columns != 'Unnamed: 0']

data = data.iloc[[3,4]]

newdata = {'bet_time_over_1000' : ['Q1','Q2','Q3','Q4'], 'correct_amounts': data.iloc[0]*data.iloc[1].values, 'incorrect_amounts': data.iloc[0] - (data.iloc[0]*data.iloc[1]).values}
newdata = pd.DataFrame(newdata) 
print(newdata)
pivot_data = newdata.set_index('bet_time_over_1000').T
sns.heatmap(data = pivot_data, annot=True, fmt="g", cmap='viridis')


plt.show()

###################################################################################################

### Plots for Category Market Data



