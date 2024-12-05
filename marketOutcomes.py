import pandas as pd
import ast
import os
import json

# Folder containing JSON files
folder_path = 'data/bronze/'

# Read all JSON files in the folder into a single DataFrame
data_frames = []
for file_name in os.listdir(folder_path):
    if file_name.endswith('.json'):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as f:
            data = json.load(f)
            df = pd.DataFrame(data)
            data_frames.append(df)

# Combine all data frames into one
combined_df = pd.concat(data_frames, ignore_index=True)

## Code for finding percentage of correct predictions based on the combined JSON data

def findOutcome(contract):
    # Check if the contract exists in the combined DataFrame
    if contract in combined_df['marketMakerAddress'].values:
        # Locate the first occurrence of the contract
        index = combined_df[combined_df['marketMakerAddress'] == contract].index[0]
        value = combined_df.at[index, 'outcomePrices']
        
        # Evaluate the outcomePrices list and determine the outcome
        value = ast.literal_eval(value)
        outcome = 0 if float(value[0]) > 0.5 else 1
    else:
        print(f"Contract {contract} not in data.")
        outcome = None

    return outcome

def allOutcomes():
    # Dictionary to store the outcomes for each contract
    marketOutcomes = {}

    # Iterate over all unique contracts in combined_df
    for contract in combined_df['marketMakerAddress'].unique():
        outcome = findOutcome(contract)
        if outcome is not None:
            marketOutcomes[contract] = outcome

    # Convert the dictionary into a DataFrame
    marketOutcomesDF = pd.DataFrame(list(marketOutcomes.items()), columns=['marketMakerAddress', 'outcome'])

    return marketOutcomesDF

# Get the outcomes DataFrame
marketOutcomes = allOutcomes()

# Display the combined outcomes DataFrame
marketOutcomes.to_csv('marketOutcomesDF.csv')
