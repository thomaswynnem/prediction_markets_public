## Graphing Data for Visualization

## All Contracts Visualization First

import seaborn as sns 
import matplotlib.pyplot as plt 
import pandas as pd


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

data = pd.read_csv("data/silver/allContracts/correctsRates.csv")

data = data.loc[:,data.columns != 'BettorCorrectRate', 'contractCorrectRate']

adjusted = data.melt(var_name = 'Distribution', value_name='cCRbyDistr')

