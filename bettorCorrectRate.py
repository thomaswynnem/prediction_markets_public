import pandas as pd

def isCorrect(contract, totalBuyScansDF, allOutcomes):
    if contract not in totalBuyScansDF['smartContract'].values:
            return None, None
    contractDF = totalBuyScansDF[(totalBuyScansDF['smartContract'] == contract)]

    contractIndex = allOutcomes[allOutcomes['marketMakerAddress'].str.lower() == contract.lower()].index
    if len(contractIndex) == 0:
        return None, None

    outcome = allOutcomes.iloc[contractIndex[0]]['outcome']

    value_counts = contractDF['outcomeIndex'].value_counts()

    yesbets = value_counts.get(0,0)
    nobets = value_counts.get(1,0)
    totalbets = yesbets+nobets

    print(yesbets)
    print(nobets)



    if outcome == 0:
        return yesbets, totalbets
    else:
        return nobets, totalbets
    

def correctPerc(totalBuyScansDF, allOutcomes):
    try:    
        contracts = totalBuyScansDF['smartContract'].unique()
    except:
        return 0,0,0
    totalCorrect = 0
    totalBuys = 0
    for contract in contracts:
        correct, amount = isCorrect(contract, totalBuyScansDF, allOutcomes)
        if amount is None:
             continue
        elif correct is None:
            totalBuys+=amount
        else:
            totalCorrect += correct
            totalBuys+=amount
            
    return totalCorrect/totalBuys, totalBuys, totalCorrect