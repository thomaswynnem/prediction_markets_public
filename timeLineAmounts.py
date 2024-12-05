import pandas as pd

def amountFunc(quad1,quad2,contractDF):

    total = 0
    for iter in range(int(quad1),int(quad2+1)):
        amount = contractDF.iloc[iter]['investmentAmount']
        amount = int(amount)
        if not amount:
            continue
        total+=amount
    return total


def contractTotal(contract, totalBuyScans):

    contractDF = totalBuyScans[totalBuyScans['smartContract']==contract]
    

    rows = len(contractDF)

    if rows == 0:
        return None

    quadrants = [0]

    
    halfRows = rows//2
    quarterRows = rows//4
    threeQuartersRows = (3*rows)//4

    quadrants.append(quarterRows)
    quadrants.append(halfRows)
    quadrants.append(threeQuartersRows)
    quadrants.append(rows-1)

    quadrantAmounts = []

    for iv in range(4):
        total = amountFunc(quadrants[iv], quadrants[iv+1],contractDF)
        quadrantAmounts.append(total)


    return quadrantAmounts


def contractAmountSwitcher(totalBuyScans):

    try:
        contracts = totalBuyScans['smartContract'].unique()
    except:
        return[0,0,0,0], [0,0,0,0]
    
    contracts = totalBuyScans['smartContract'].unique()
    quadrantTotalAmounts = []
    for contract in contracts:
        quadrantAmounts = contractTotal(contract, totalBuyScans)
        quadrantTotalAmounts.append(quadrantAmounts)

    sumT1 = 0
    sumT2 = 0
    sumT3 = 0
    sumT4 = 0

    for iv in range(len(quadrantTotalAmounts)):
        sumT1+=quadrantTotalAmounts[iv][0]
        sumT2+=quadrantTotalAmounts[iv][1]
        sumT3+=quadrantTotalAmounts[iv][2]
        sumT4+=quadrantTotalAmounts[iv][3]
    
        
        

    return [sumT1,sumT2,sumT3,sumT4]
