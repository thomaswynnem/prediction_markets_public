# Initialize necessary tools
import requests
import pandas as pd


# For PolygonScan
polyApiKey = '77DPF8U89P2VMDDPFAP11DCNM38Z8C6WRV'

# Addresses of USDC Coin and Transfer Event on Polygon
usdcAddress = '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359'
transferEvent = '0x8c5261668696ce22758910d05bab8f186d6eb247ceac2af2e82c7dc17669b036'

# API Sources
polyScanUrl = 'https://api.polygonscan.com/api?'
gammaURL = 'https://gamma-api.polymarket.com/markets?'

marketMakerArray = []

## Getting 50,000 Dollar Prediction Markets in 2020

years = [2023,2022,2021]


def contractFetcher(year, marketMakerArray): 
        if year == 2023:
                marketsPossible = requests.get(f'{gammaURL}closed=true&liquidity_num_min=3&volume_num_min=10000&volume_num_max=100000&start_date_min=2023-01-01T00:00:00Z&end_date_max=2023-01-06T00:00:00Z&limit=1000000000')
                
        else:
                marketsPossible = requests.get(f'{gammaURL}closed=true&liquidity_num_min=3&volume_num_min=10000&volume_num_max=100000&start_date_min={year}-01-01T00:00:00Z&end_date_max={year+1}-01-01T00:00:00Z&limit=1000000000')

        marketsPossibleData = marketsPossible.json()
        print(marketsPossibleData)

        df = pd.DataFrame(marketsPossibleData)
        print(df)       

        df.to_excel(f'marketsPossibleData{year}.xlsx')

        for market in marketsPossibleData:
                marketMakerAddress= market.get('marketMakerAddress')
                if marketMakerAddress == '':
                        continue
                marketMakerArray.append(marketMakerAddress)
        
        return marketMakerArray


def main():
    for year in years: 
            marketMakerArray = contractFetcher(year, marketMakerArray)

    marketMakerDF = pd.DataFrame(marketMakerArray)
    marketMakerDF.to_excel('marketMakerAddress.xlsx', index=False)

    return marketMakerArray

    exit