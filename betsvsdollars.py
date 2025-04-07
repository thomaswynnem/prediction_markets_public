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


def decisionDistribution(contract, totalBuyScansDF):
    if contract not in totalBuyScansDF['smartContract'].values:
        print("fail")
        return None
    contractDF = totalBuyScansDF[totalBuyScansDF['smartContract'] == contract]

    decisions = contractDF['outcomeIndex'].value_counts()
    print(f"This is decisions amount {decisions.sum()}")
    try:
        return decisions[0] / decisions.sum(), decisions.sum()
    except (ZeroDivisionError, IndexError, KeyError, TypeError) as e:
        print("Error: ", e)
        return 0,0
    
    
      
import pandas as pd

def compareInvestmentandDecisionDistribution(marketOutcomes, totalBuyScansDF):

    contractPredictions = pd.DataFrame(columns=['smartContract', 'individualCorrectRate', 'correctMoneyDistribution', 'amountOfInvestors'])
    marketOutcomes['distribution'] = None
    
    for contract in totalBuyScansDF['smartContract'].unique():
        distribution = investmentDistribution(contract, totalBuyScansDF)
        marketOutcomes.loc[marketOutcomes['marketMakerAddress'] == contract, 'distribution'] = distribution
        decisions, amountOfInvestors = decisionDistribution(contract, totalBuyScansDF)
        print(f"This is distribution {distribution}")
        print(f"This is decisions {decisions}")

        index = marketOutcomes[marketOutcomes['marketMakerAddress'] == contract]
        realOutcomeIndex = index['index'].iloc[0]

        if realOutcomeIndex == 1:
            distribution = 1 - distribution
            decisions = 1 - decisions

        contractPredictions = pd.concat([contractPredictions, pd.DataFrame({'smartContract': [contract], 'individualCorrectRate': [decisions], 'correctMoneyDistribution': [distribution], 'amountOfInvestors': [amountOfInvestors]})], ignore_index=True)


    return contractPredictions, marketOutcomes