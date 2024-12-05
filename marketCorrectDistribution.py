import pandas as pd

def investmentDistribution(contract, totalBuyScansDF):
    if contract not in totalBuyScansDF['smartContract'].values:
        print("fail")
        return None
    contractDF = totalBuyScansDF[totalBuyScansDF['smartContract'] == contract]

    contractYesDF = contractDF[contractDF['outcomeIndex'] == 0]
    contractNoDF = contractDF[contractDF['outcomeIndex'] == 1]

    yesmoney = contractYesDF['investmentAmount'].sum()
    nomoney = contractNoDF['investmentAmount'].sum()
    
    totalInvestment = yesmoney + nomoney
    if totalInvestment == 0:
        return None

    distribution = yesmoney / totalInvestment
    return distribution

def correctContracts(totalBuyScansDF, atPerc, marketOutcomes):
    try:    
        contracts = totalBuyScansDF['smartContract'].unique()
    except:
        return 0,0
    highPercContracts = 0
    correctHighPerc = 0
    distributions = []


    for contract in contracts:
        distribution = investmentDistribution(contract, totalBuyScansDF)
        distributions.append(distribution)

        if distribution is None:
            continue
        index = marketOutcomes[marketOutcomes['marketMakerAddress'] == contract].index
        if len(index) == 0:
            
            continue

        index = index[0]
        realOutcome = int(marketOutcomes.iloc[index]['outcome'])
        

        if realOutcome !=1 and realOutcome!=0:
            continue
        
        if atPerc == .85:
            if distribution >= atPerc and distribution <= atPerc+.15:
                highPercOutcome = 0
            elif distribution<= 1-atPerc and distribution >= 1-atPerc-.15:
                highPercOutcome=1
            else:
                highPercOutcome = 100
        
        else:
            if distribution >= atPerc and distribution <= atPerc+.05:
                highPercOutcome = 0
            elif distribution<= 1-atPerc and distribution >= 1-atPerc-.05:
                highPercOutcome=1
            else:
                highPercOutcome = 100

        if highPercOutcome==0 or highPercOutcome==1:
            highPercContracts += 1
            if int(highPercOutcome) == int(realOutcome):
                correctHighPerc += 1
            
        
    if highPercContracts == 0:
        
        return 0

    highPercAccuracy = (correctHighPerc/highPercContracts)*100

    return highPercAccuracy, highPercContracts


      

def correctIntervals(totalBuyScansDF, marketOutcomes):
    correctRates = []
    intervals = []

    for rate in range (50,90,5):
        rate = rate/100
        highPercAccuracy, highPercContracts = correctContracts(totalBuyScansDF, rate, marketOutcomes)
        intervals.append(rate)
        correctRates.append(highPercAccuracy)
        
        
        print(f"High Perc Prediction accuracy: {highPercAccuracy:.2f}%")
        print(highPercContracts)

    return correctRates, intervals