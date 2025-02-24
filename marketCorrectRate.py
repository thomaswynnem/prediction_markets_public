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
    print("Correct Contracts")
    try:    
        contracts = totalBuyScansDF['smartContract'].unique()
    except:
        return 0,0
    correct_predictions = 0
    total_contracts = 0
    print("Looper")
    for contract in contracts:
        distribution = isCorrect(contract, totalBuyScansDF)
        if distribution is None:
            continue
        print(type(contract))
        print(contract)
        row = marketOutcomes[marketOutcomes['marketMakerAddress'] == contract]

        print(row)
        outcomeIndex = int(row['index'].values[0])
        

        # Determine predicted outcome based on distribution
        if distribution > .5:
            predictedOutcome = 0
        else:
            predictedOutcome = 1

        
        print(f"Contract: {contract}")
        print(f"Distribution: {distribution:.2f}, Predicted Outcome: {predictedOutcome}, Real Outcome: {outcomeIndex}")

        # Compare predicted outcome to real outcome
        if int(predictedOutcome) == int(outcomeIndex):
            correct_predictions += 1
        total_contracts += 1

    if total_contracts == 0:
        print("No contracts to evaluate.")
        return 0,0

    accuracy = (correct_predictions / total_contracts) * 100
    print(len(contracts))
    return accuracy

