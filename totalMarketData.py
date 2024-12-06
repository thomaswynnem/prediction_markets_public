import pandas as pd
import os

from bettorCorrectRate import correctPerc

from marketCorrectDistribution import correctIntervals

from marketCorrectRate import correctContracts

from sizedBuyersDistribution import intervalPerc

from timelineCorrectness import contractSwitcher

from largeInvQuarters import contractSizedSwitcher

from timeLineAmounts import contractAmountSwitcher

from contracts import marketDetails

from categories import runCategories

os.mkdir('data/silver/allContracts')

marketsDF = pd.read_csv('data/silver/markets_with_categories.csv')

marketOutcomes = pd.read_csv('data/silver/marketOutcomes.csv')

totalBuyScansDF = pd.read_csv('data/silver/contract_buy.csv')

bettorCorrectRate, totalBuys, totalCorrect = correctPerc(totalBuyScansDF, marketOutcomes)

contractCorrectRates, intervals = correctIntervals(totalBuyScansDF, marketOutcomes)

contractCorrectRate = correctContracts(totalBuyScansDF, marketOutcomes)

correctRateDF = pd.DataFrame([bettorCorrectRate,contractCorrectRate,[contractCorrectRates],[intervals]], index=["BettorCorrectRate", "contractCorrectRate","cCRbyDistr","Distribution"])
correctRateDF.to_csv('data/silver/allContracts/correctsRates.csv')

intervalBracket, correctRate, buygr = intervalPerc(totalBuyScansDF, marketOutcomes)
quarterCorrect, quarterTotal = contractSwitcher(totalBuyScansDF, marketOutcomes)
quarterSizedCorrect, quarterSizedTotal = contractSizedSwitcher(totalBuyScansDF, marketOutcomes, 1500)
quarterAmounts = contractAmountSwitcher(totalBuyScansDF)

quarterPerc = []
quarterSizedPerc = []
for iv in range(4):

    quarterPerc.append(quarterCorrect[iv]/quarterTotal[iv])
    quarterSizedPerc.append(quarterSizedCorrect[iv]/quarterSizedTotal[iv])


timelineDF = pd.DataFrame([quarterAmounts, quarterTotal, quarterPerc, quarterSizedTotal, quarterSizedPerc], index=["Money","Bets", "PercC", "BigBets","BigPercC"], columns=["Quarter1", "Quarter2", "Quarter3", "Quarter4"])
timelineDF.to_csv(f'data/silver/allContracts/timeline_quarterDF.csv')

dollarlyDF = pd.DataFrame([buygr, correctRate], index=["Number of Bets", "Correct Rate"], columns=["0-100", "100-200", "200-300","300-400","400-500","500-600","600-700","700-800","800-900","900-1000"])
dollarlyDF.to_csv(f'data/silver/allContracts/dollarly_valueDF.csv')

marketDetails()

runCategories()
