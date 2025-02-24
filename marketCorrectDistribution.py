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
    contractsInRealm = 0
    correctPerc = 0
    distributions = []
    print("Here")

    for contract in contracts:
        distribution = investmentDistribution(contract, totalBuyScansDF)
        if distribution is None:
            continue
        distributions.append(distribution)

        index = marketOutcomes[marketOutcomes['marketMakerAddress'] == contract]

        print(index)

        try:
            print(index['index'].iloc[0])
            realOutcome = index['index'].iloc[0]
            print(f"The outcome index: {realOutcome}")
        except (ValueError, TypeError):
            print("The  seems to be an issue fetching index from market outcomes")
            continue

        realOutcome = int(realOutcome)
    
        if distribution >= atPerc and distribution <= atPerc+.05:
            predIndex = 0
        elif distribution<= 1-atPerc and distribution >= 1-atPerc-.05:
            predIndex = 1
        else:
            predIndex = 100

        if predIndex==0 or predIndex==1:
            contractsInRealm += 1
            if int(predIndex) == int(realOutcome):
                correctPerc += 1
            
        
    if contractsInRealm == 0:
        print (f"No Contracts in realm {atPerc}")
        return 0,0

    highPercAccuracy = (correctPerc/contractsInRealm)*100

    return highPercAccuracy, contractsInRealm


      

def correctIntervals(totalBuyScansDF, marketOutcomes):
    print("Correct Intervals")
    correctRates = []
    intervals = []

    for rate in range (50,90,5):
        print(f"Rate: {rate}")
        rate = rate/100
        print(f"Calling correct contracts with buy scans as: {totalBuyScansDF} and market outcomes as: {marketOutcomes}")
        highPercAccuracy, contractsInRealm = correctContracts(totalBuyScansDF, rate, marketOutcomes)
        intervals.append(rate)
        correctRates.append(highPercAccuracy)
        
        
        print(f"High Perc Prediction accuracy: {highPercAccuracy:.2f}%")
        print(contractsInRealm)

    return correctRates, intervals