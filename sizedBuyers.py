import requests
import pandas as pd
import json

marketOutcomes = []

def getMarketOutcomes(marketOutcomes, year):
    markets = pd.read_excel(f"marketsPossibleData{year}.xlsx")
    for market in markets['outcomePrices']:
        modernmarket = json.loads(market)
        if float(modernmarket[0]) < .5:
            marketOutcomes.append(int(0))
        else:
            marketOutcomes.append(int(1))
    return marketOutcomes

def checkPolitics(eventNum):
    if eventNum <= 49:
        return 0
        
    elif eventNum <= 149:
        markets = pd.read_excel(f"PolyMarket/marketsPossibleData2022.xlsx")
        marketCats = markets['category']
        
        category = marketCats[eventNum-50]
    else: 
        markets = pd.read_excel(f"PolyMarket/marketsPossibleData2021.xlsx")
        marketCats = markets['category']
        
        category = marketCats[eventNum-151]
    
    if category == 'US-current-affairs':
        return 1
    else:
        return 0



getMarketOutcomes(marketOutcomes, 2023)
getMarketOutcomes(marketOutcomes, 2022)
getMarketOutcomes(marketOutcomes, 2021)

df = pd.DataFrame(marketOutcomes)
df.to_excel('alloutcomes.xlsx')

print(marketOutcomes)

bigMoneyList = []
biggerMoneyList =[]

for x in range(206):

    excelString = f'Buy/contractbuyinfo{x}.xlsx'
    content = pd.read_excel(excelString)

    print(f'contract number: {x}')
    
    keys = content.keys()
    if (keys.empty):
        continue
    
    addresses = content['buyer'].tolist()
    print(len(addresses))
    investmentAmounts = content['investmentAmount'].tolist()
    print(len(investmentAmounts))
    decision = content['outcomeIndex'].tolist()
    print(len(decision))
    usedWallets =[]
    for iv in range(len(investmentAmounts)):
        
        investmentAmount = investmentAmounts[iv]/1000000
        if investmentAmount >1000 and investmentAmount<4500:
            print(investmentAmount)
            wallet = addresses[iv]
            outcomechoice = decision[iv]
            print(outcomechoice)
            if wallet in usedWallets:
                continue
            dict = {'investment': investmentAmount, 'walletVal': wallet, 'contract': x, 'outcomeChoice': outcomechoice, 'realOutcome': marketOutcomes[x]}
            usedWallets.append(wallet)
            bigMoneyList.append(dict)
            if investmentAmount > 5000:
                biggerMoneyList.append(dict)
        

print(len(bigMoneyList))
print(biggerMoneyList)
print(len(biggerMoneyList))

totalpayouts = 0
totalpayins = len(bigMoneyList)

df = pd.DataFrame(bigMoneyList)
df.to_excel("bettingindis.xlsx")








for val in range(totalpayins):
    outcome = bigMoneyList[val]['realOutcome']
    investedOutcome = bigMoneyList[val]['outcomeChoice']
    
    if investedOutcome == outcome:
        print('check')
        totalpayouts+=1
        

print(totalpayouts/totalpayins)
print(len(marketOutcomes))

print(totalpayins)
print(marketOutcomes)

thing = []
for it in range(len(bigMoneyList)):
    thing.append(bigMoneyList[it]['outcomeChoice'])

print(thing)







