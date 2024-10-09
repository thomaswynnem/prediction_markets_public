from web3 import Web3
import json
import requests
import pandas as pd


totalMarkets = pd.read_excel("marketMakerAddress.xlsx")
marketOutcomes = pd.read_excel('alloutcomes.xlsx')
marketOutcomes = marketOutcomes[0]

def main():
    totalbets = 0
    totalcorrect = 0
    finalbets = 0
    correctfinalbets = 0
   
    for market in range(206):
        repeatingWallets = fetchRepeats(market)
        
        if not repeatingWallets:
            continue
        for wallet in repeatingWallets:
            correctness = repeatingWallets[wallet]
            totalbets+=len(correctness)
            priorbet = correctness[0]
            currentbet = correctness[0]
            iter = 0
            change =0
            
            for answer in correctness:
                currentbet = correctness[iter]
                
                
                if currentbet!= priorbet:
                    change+=1
                if answer == 1:
                    totalcorrect+=1
                priorbet = currentbet
                iter+=1
            
            if change > 0:
                
                finalbets +=1 
                correctfinalbets += correctness[iter-1]

    
    correctrateofmulti = totalcorrect/totalbets

    finalofchangers = correctfinalbets/finalbets

    
    return [correctrateofmulti, finalofchangers]


def fetchRepeats(market):
    purchases = pd.read_excel(f'Buy/contractbuyinfo{market}.xlsx')
    if purchases.empty:
        return None
    wallets = purchases['buyer'].tolist()
    outcomePredictions = purchases['outcomeIndex'].tolist()
    outcome = marketOutcomes[market].tolist()
    totalTimes = {}
    repeatingWallets = {}

    for it in range(len(wallets)):
        wallet = wallets[it]
        predictedOutcome = outcomePredictions[it]
        if predictedOutcome == outcome:
            correctness = 1
        else:
            correctness = 0
        if wallet in totalTimes:
            totalTimes[wallet] += 1
            if wallet not in repeatingWallets:
                listofcorrectness = []
                listofcorrectness.append(correctness)
                repeatingWallets[wallet] = listofcorrectness
            else:
                already = repeatingWallets[wallet]
                already.append(correctness)
                repeatingWallets[wallet] = already
        else:
            totalTimes[wallet] = 1

    return repeatingWallets



main()