import pandas as pd

def percentageFunc(quad1,quad2,outcome,contractDF):
    totalCorrect = 0
    total = 0
    for iter in range(int(quad1),int(quad2+1)):
        predOutcome = contractDF.iloc[iter]['outcomeIndex']
        predOutcome = int(predOutcome)


        if int(predOutcome)!=0 and int(predOutcome)!=1:

            continue
        total+=1

        if predOutcome == outcome:
            totalCorrect+=1
    if total == 0:

        return None

    return totalCorrect, total

def winner(marketOutcomes, contract):

    outcome = int(marketOutcomes.loc[marketOutcomes['marketMakerAddress'] == contract, 'outcome'])


    if outcome !=1 and outcome !=0:

        return None
    return outcome

def contractCorrectness(contract, totalBuyScans, marketOutcomes):

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
        totalCorrect, total = percentageFunc(quadrants[iv], quadrants[iv+1],outcome,contractDF)
        quadrantCorrect.append(totalCorrect)
        quadrantTotal.append(total)



    return quadrantCorrect, quadrantTotal


def contractSwitcher(totalBuyScans, marketOutcomes):
    try:
        contracts = totalBuyScans['smartContract'].unique()
    except:
        return[0,0,0,0], [0,0,0,0]
    contracts = totalBuyScans['smartContract'].unique()
    quarterSizedCorrect = []
    quarterSizedTotal = []
    for contract in contracts:
        quadrantCorrect, quadrantTotal = contractCorrectness(contract, totalBuyScans, marketOutcomes)
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
