from web3 import Web3
import json
import requests
import pandas as pd

## Now that there are 3 Excel sheets full of 100 examples of prediction markets, I will begin to grab information out of them using
## the polygonscan api:
# Over 1000 Dollar Investments
# Payouts (which was right)
# How many different wallets participated
# What was the money distribution
# Any repeat investors???

content = pd.read_excel("marketMakerAddress.xlsx")

eventSignature = "FPMMBuy(address,uint256,uint256,uint256,uint256)"
eventSignatureHash = Web3.keccak(text=eventSignature).hex()
smartContracts = content[0].tolist()
i =0



def analyzeContract(smartContract, i):
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

        print(logs.keys())

        web3 = Web3(Web3.HTTPProvider(url))
        contract = web3.eth.contract(address=smartContract, abi=[abi])
        totalLogs = []
        for log in logs['result']:
            logData = log["data"]
            decodedLog = contract.events.FPMMBuy().process_log(log)
            info = decodedLog['args']
            totalLogs.append(info)
            
            
        df = pd.DataFrame(totalLogs)
        excelstring = f'contractbuyinfo{i}'
        df.to_excel(f'{excelstring}.xlsx')
        
    
    except Exception as e:
        print(f"Error for contract {smartContract}: {e}")
        quit

i = 0
for smartContract in smartContracts:
    analyzeContract(smartContract, i)
    i+=1



    
