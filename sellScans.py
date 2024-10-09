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
smartContracts = content[0].tolist()
i =0
def analyzeSellContract(smartContract, i):
    try:
        payload = {
            "method": "eth_getLogs",
            "params": [
                {
                    "fromBlock": "0", 
                    "toBlock": "latest", 
                    "address": smartContract,
                    "topics": [
                        "0xadcf2a240ed9300d681d9a3f5382b6c1beed1b7e46643e0c7b42cbe6e2d766b4"
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
                    "name": "seller",
                    "type": "address"
                },
                {
                    "indexed": False,
                    "name": "returnAmount",
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
                    "name": "outcomeTokensSold",
                    "type": "uint256"
                }
            ],
            "name": "FPMMSell",
            "type": "event"
        }

        print(logs.keys())

        web3 = Web3(Web3.HTTPProvider(url))
        contract = web3.eth.contract(address=smartContract, abi=[abi])
        totalLogs = []
        for log in logs['result']:
            logData = log["data"]
            decodedLog = contract.events.FPMMSell().process_log(log)
            info = decodedLog['args']
            totalLogs.append(info)
            
            
        df = pd.DataFrame(totalLogs)
        excelstring = f'contractsellinfo{i}'
        df.to_excel(f'{excelstring}.xlsx')
        

    except Exception as e:
        print(f"Error for contract {smartContract}: {e}")
        quit

i = 0
for smartContract in smartContracts:
    i +=1
    analyzeSellContract(smartContract, i)




    
