import pandas as pd

from timelineCorrectness import winner

def amountFunc(quad1,quad2,outcome,contractDF, size):
    largeFreq = 0
    largeCorrect = 0


    for iter in range(int(quad1),int(quad2+1)):
        amount = contractDF.iloc[iter]['investmentAmount']
        predictedOutcome = contractDF.iloc[iter]['outcomeIndex']
        amount = int(amount)
        predictedOutcome = int(predictedOutcome)
        
        if not amount:

            continue
        if predictedOutcome!=1 and predictedOutcome!=0:

            continue

        if amount/1000000 > size:
            largeFreq +=1
            if predictedOutcome == outcome:
                largeCorrect += 1
    return largeCorrect, largeFreq

def contractCorrectness(contract, totalBuyScans, marketOutcomes, size):

    outcome = winner(marketOutcomes, contract)

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

    quadrantCorrect = []
    quadrantTotal = []
   

    for iv in range(4):
        largeCorrect, largeFreq = amountFunc(quadrants[iv], quadrants[iv+1],outcome,contractDF, size)
        quadrantCorrect.append(largeCorrect)
        quadrantTotal.append(largeFreq)
        


    return quadrantCorrect, quadrantTotal


def contractSizedSwitcher(totalBuyScans, marketOutcomes, size):
    try:
        contracts = totalBuyScans['smartContract'].unique()
    except:
        return[0,0,0,0], [0,0,0,0]
    quarterSizedCorrect = []
    quarterSizedTotal = []
    for contract in contracts:
        quadrantCorrect, quadrantTotal = contractCorrectness(contract, totalBuyScans, marketOutcomes, size)
    
        quarterSizedCorrect.append(quadrantCorrect)
        quarterSizedTotal.append(quadrantTotal)

    sumC1 = 0
    sumC2 = 0
    sumC3 = 0
    sumC4 = 0

    sumT1 = 0
    sumT2 = 0
    sumT3 = 0
    sumT4 = 0

    for iv in range(len(quarterSizedCorrect)):
        sumC1+=quarterSizedCorrect[iv][0]
        sumC2+=quarterSizedCorrect[iv][1]
        sumC3+=quarterSizedCorrect[iv][2]
        sumC4+=quarterSizedCorrect[iv][3]
        sumT1+=quarterSizedTotal[iv][0]
        sumT2+=quarterSizedTotal[iv][1]
        sumT3+=quarterSizedTotal[iv][2]
        sumT4+=quarterSizedTotal[iv][3]

    

    return [sumC1,sumC2,sumC3,sumC4], [sumT1,sumT2,sumT3,sumT4]