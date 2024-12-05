from web3 import Web3
import json
import requests
import pandas as pd


eventSignature = "FPMMBuy(address,uint256,uint256,uint256,uint256)"
eventSignatureHash = Web3.keccak(text=eventSignature).hex()

df = pd.read_csv("marketOutcomes.csv")
addresses = df['marketMakerAddress'].unique()




def analyzeContract(smartContract):
    try:
        payload = {
            "method": "eth_getLogs",
            "params": [
                {
                    "fromBlock": "0", 
                    "toBlock": "latest", 
                    "address": smartContract,
                    "topics": [
                        f'0x{eventSignatureHash}'
                    ]
                }
            ],
            "id": 1,
            "jsonrpc": "2.0"
        }

        url = "https://polygon-rpc.com/"

        
        headers = {"Content-Type": "application/json"}

        
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        
        if response.status_code == 200:
          
            logs = response.json()
            print(json.dumps(logs, indent=2))  
        else:
            print(f"Error: {response.status_code}, {response.text}")

        abi = {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "name": "buyer",
                    "type": "address"
                },
                {
                    "indexed": False,
                    "name": "investmentAmount",
                    "type": "uint256"
                },
                {
                    "indexed": False,
                    "name": "feeAmount",
                    "type": "uint256"
                },
                {
                    "indexed": True,
                    "name": "outcomeIndex",
                    "type": "uint256"
                },
                {
                    "indexed": False,
                    "name": "outcomeTokensBought",
                    "type": "uint256"
                }
            ],
            "name": "FPMMBuy",
            "type": "event"
        }


        web3 = Web3(Web3.HTTPProvider(url))
        contract = web3.eth.contract(address=smartContract, abi=[abi])
        totalLogs = []
        for log in logs['result']:
            decodedLog = contract.events.FPMMBuy().process_log(log)
            info = decodedLog['args']
            info["smartContract"] = smartContract
            totalLogs.append(info)
            
        
        df = pd.DataFrame(totalLogs)
        

        return df
        
    
    except Exception as e:
        print(f"Error for contract {smartContract}: {e}")
        return pd.DataFrame()




dfs = []

for smartContract in addresses:
    df = analyzeContract(smartContract)
    if not df.empty:
        dfs.append(df)

# Concatenate all the dataframes at once
if dfs:
    totalBuyScansDF = pd.concat(dfs, ignore_index=True)
else:
    totalBuyScansDF = pd.DataFrame()  # In case no data was found, return an empty DataFrame

totalBuyScansDF.to_csv('totalBuyScans.csv')