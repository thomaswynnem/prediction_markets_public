import pandas as pd



def manualCategoryFixer(marketsDF):
    

    for index, row in marketsDF.iterrows():
        if row['category'] == 'US-current-affairs':
            marketsDF.at[index, 'category'] = 'Politics'
            print('US-current-affairs')

        elif row['category'] == 'Ukraine & Russia':
            marketsDF.at[index, 'category'] = 'Politics'
            print('Ukraine & Russia')

        elif row['category'] == 'Global Politics':
            marketsDF.at[index, 'category'] = 'Politics'
            print('Global Politics')

        elif row['category'] == 'Tech':
            marketsDF.at[index, 'category'] = 'Science-Tech'
            print('Tech')

        elif row['category'] == 'Space':
            marketsDF.at[index, 'category'] = 'Science-Tech'
            print('Space')

        elif row['category'] == 'Science':
            marketsDF.at[index, 'category'] = 'Science-Tech'
            print('Science')

        elif row['category'] == 'Coronavirus-':
            marketsDF.at[index, 'category'] = 'Coronavirus'
            print('Coronavirus-')

        elif row['category'] == 'Chess':
            marketsDF.at[index, 'category'] = 'Sports'
            print('Chess')

        elif row['category'] == 'Olympics':
            marketsDF.at[index, 'category'] = 'Sports'
            print('Olympics')

        elif row['category'] == 'Poker':
            marketsDF.at[index, 'category'] = 'Sports'
            print('Poker')

        elif row['category'] == 'Art':
            marketsDF.at[index, 'category'] = 'Pop-Culture'
            print('Art')

        elif row['category'] == 'Pop-Culture ':
            marketsDF.at[index, 'category'] = 'Pop-Culture'
            print('Pop-Culture ')


    marketsDF.to_csv('data/silver/markets_with_categories.csv')

    return marketsDF

        
