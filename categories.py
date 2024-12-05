import pandas as pd

import os

from timelineCorrectness import contractSwitcher

from largeInvQuarters import contractSizedSwitcher

from timeLineAmounts import contractAmountSwitcher


def runCategories():
    os.mkdir('data/silver/Subjects')
    marketsDF = pd.read_csv("markets_with_categories.csv")

    categories = marketsDF['category'].unique()

    print(categories)

    from sizedBuyersDistribution import intervalPerc



    marketOutcomes = pd.read_csv('marketOutcomes.csv')
    totalBuyScansDF = pd.read_csv('contract_buy.csv')


    for category in categories:
        topicBS = pd.DataFrame()
        newinfo = marketsDF[(marketsDF['category'] == category)]
        smartContracts = newinfo['marketMakerAddress'].unique()
        print(smartContracts)
        for contract in smartContracts:

            contractBuyScans = totalBuyScansDF[totalBuyScansDF['smartContract'] == contract]
            topicBS = pd.concat([topicBS, contractBuyScans], ignore_index=True)

        if 'smartContract' not in contractBuyScans:
            continue

        intervalBracket, correctRate, buygr = intervalPerc(topicBS, marketOutcomes)
        quarterCorrect, quarterTotal = contractSwitcher(topicBS, marketOutcomes)
        quarterSizedCorrect, quarterSizedTotal = contractSizedSwitcher(topicBS, marketOutcomes, 1500)
        quarterAmounts = contractAmountSwitcher(topicBS)

        print(intervalBracket)
        print(correctRate)
        print(buygr)
        if len(quarterCorrect) != 0:
            quarterPerc = []
            quarterSizedPerc = []
            for iv in range(4):
                if quarterTotal[iv] == 0:
                    quarterPerc.append(0)
                else:
                    quarterPerc.append(quarterCorrect[iv]/quarterTotal[iv])
                if quarterSizedTotal[iv] == 0:
                    quarterSizedPerc.append(0)
                else:
                    quarterSizedPerc.append(quarterSizedCorrect[iv]/quarterSizedTotal[iv])
            timelineDF = pd.DataFrame([quarterAmounts, quarterTotal, quarterPerc, quarterSizedTotal, quarterSizedPerc], index=["Money","Bets", "PercC", "BigBets","BigPercC"], columns=["Quarter1", "Quarter2", "Quarter3", "Quarter4"])
            timelineDF.to_csv(f'data/silver/Subjects/{category}_quarterDF.csv')

        if buygr != None and correctRate != None:
            topicDF = pd.DataFrame([buygr, correctRate], index=["Number of Bets", "Correct Rate"], columns=["0-100", "100-200", "200-300","300-400","400-500","500-600","600-700","700-800","800-900","900-1000"])
            topicDF.to_csv(f'data/silver/Subjects/{category}_valueDF.csv')