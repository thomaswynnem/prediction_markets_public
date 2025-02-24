import pandas as pd
import numpy as np
from timelineCorrectness import winner
def intervalCorrectness(contract, totalBuyScansDF, allOutcomes, sizeA,sizeB):
    if contract not in totalBuyScansDF['smartContract'].values:
            return None, None
    contractDF = totalBuyScansDF[(totalBuyScansDF['smartContract'] == contract)]
    amountDF = contractDF[(contractDF['investmentAmount'] > sizeA*10**6) & (contractDF['investmentAmount'] < sizeB*10**6)]
    if amountDF.empty:
         return 0, 0

    outcome = winner(allOutcomes, contract)
    if outcome is None:
        return 0,0
    value_counts = amountDF['outcomeIndex'].value_counts()


    yesbets = int(value_counts.get(0,0))
    nobets = int(value_counts.get(1,0))
    totalbets = yesbets+nobets
    

    if outcome == 0:
        return int(yesbets), int(totalbets)
    else:
        return int(nobets), int(totalbets)


def intervalPerc(totalBuyScansDF, allOutcomes):
    if totalBuyScansDF.empty:
        return None, None, None
    contracts = totalBuyScansDF['smartContract'].unique()
    if len(contracts)==0:
        return None, None, None
    buygr = []
    intervalBracket = [0]
    correctRate = []
    for moment in range(0,1000,100):
        totalCorrect = 0
        totalBuys = 0
        nextMoment = moment+100
        intervalBracket.append(nextMoment)
        for contract in contracts:
            correct, amount = intervalCorrectness(contract, totalBuyScansDF, allOutcomes, moment, nextMoment)
            if amount is None:
                continue
            elif correct is None:
                totalBuys+=amount
            else:
                totalCorrect += correct
                totalBuys+=amount
        if totalBuys == 0:
            perc = 0
        else:
            perc = totalCorrect/totalBuys
        buygr.append(totalBuys)
        correctRate.append(perc)


    return intervalBracket, correctRate, buygr
