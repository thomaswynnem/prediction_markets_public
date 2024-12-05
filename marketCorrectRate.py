import pandas as pd


def isCorrect(contract, totalBuyScansDF):
    if contract not in totalBuyScansDF['smartContract'].values:
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

def correctContracts(totalBuyScansDF, marketOutcomes):
    try:    
        contracts = totalBuyScansDF['smartContract'].unique()
    except:
        return 0
    correct_predictions = 0
    total_contracts = 0

    for contract in contracts:
        distribution = isCorrect(contract, totalBuyScansDF)
        if distribution is None:
            continue
        index = marketOutcomes[marketOutcomes['marketMakerAddress'] == contract].index
        if len(index) == 0:
            continue

        index = index[0]
        realOutcome = int(marketOutcomes.iloc[index]['outcome'])

        if realOutcome !=1 and realOutcome != 0:
            continue
        # Determine predicted outcome based on distribution
        if distribution > .5:
            predictedOutcome = 0
        else:
            predictedOutcome = 1

        
        print(f"Contract: {contract}")
        print(f"Distribution: {distribution:.2f}, Predicted Outcome: {predictedOutcome}, Real Outcome: {realOutcome}")

        # Compare predicted outcome to real outcome
        if int(predictedOutcome) == int(realOutcome):
            correct_predictions += 1
        total_contracts += 1

    if total_contracts == 0:
        print("No contracts to evaluate.")
        return 0

    accuracy = (correct_predictions / total_contracts) * 100
    print(len(contracts))
    return accuracy

