###########################################

# This module generates several csv files that will be used to train the models.
# Running it might take some time.
# The relevant csv files are already provided. If you run this, you will overwrite them.

###########################################


import pandas as pd
pd.options.mode.chained_assignment = None
import re
import joblib

#This loads a function to lemmatize the abstracts
from clean_text import replace_ngrams, lemmatize_keywords, lemmatize_abstract

#%%

def combine_abstracts_keywords(df):
    '''
    
    A function that takes a df with Lingbuzz data and returns a tuple with
    the name of an author, their keywords and abstracts.
    
    Parameters
    ----------
    df : A dataframe

    Returns
    -------
    info_auth : tuple

    '''
    
    info_auth = []
    
    for author_in_list in df['Author'].unique().tolist():
        #print(f'Checking {author_in_list}')
        keywords = []
        abstracts = []
        
        for row in range(len(df)):
            if author_in_list == df.iloc[row, 0]:
                separated_keywords = df.iloc[row, 5].split(', ')
                keywords.append(separated_keywords)
                abstracts.append(df.iloc[row, 2])
        info = (author_in_list, keywords, abstracts)
        info_auth.append(info)
    return info_auth

#%%

#just make a function that changes the keywords as you collect the ngrams

def get_ngrams2(df):
    pattern = r', |,|; |;'
    counter = 0
    n_gram_dict = {}
    
    replace_kw_column = []
    
    for kws in df['Keywords']:
        kws = re.split(pattern, kws)
        replace_kws = []
        for token_kw in kws:
            single_words = token_kw.split(' ')
            if len(single_words) > 1:
                if token_kw in n_gram_dict.keys():
                    dummy = n_gram_dict[token_kw]
                    replace_kws.append(dummy)
                else:
                    dummy = f'ngram{counter}'
                    n_gram_dict[token_kw] = dummy
                    replace_kws.append(dummy)
                    counter += 1
            else:
                replace_kws.append(token_kw)
        replace_kws = ', '.join(replace_kws)
        replace_kw_column.append(replace_kws)
    joblib.dump(n_gram_dict, 'n_grams.pkl')
    df['Keywords_with_ngrams'] = replace_kw_column
    return n_gram_dict

#%%


def drop_authors(df, n_manuscripts):
    '''
    Drops all the authors from a dataframe that do not have at least n manuscripts in the database.

    Parameters
    ----------
    df (DataFrame): A DataFrame with a column named 'Author'
    n_manuscripts (Int) : Minimum amount of abstract in the database for an author

    Returns
    -------
    DataFrame: A dataframe with authors with at least n manuscripts in the database

    '''
    # This lists the authors of all the papers in the database
    all_authors = pd.DataFrame(ms_byauthor(source_df), columns = ['Author', 'Keywords', 'Abstract', 'Title', 'Id'])
    
    # This counts how many papers each author has
    count_authors = all_authors.groupby('Author').count()
    
    # This creates a list of all the authors with less than n manuscripts
    count_authors = count_authors[count_authors['Abstract'] < n_manuscripts]
    
    # And this drops these authors from df
    df_filtered = df[~df['Author'].isin(count_authors.index)]
    
    return df_filtered


#%%

###############################
# This is for manuscripts_df
###############################

def ms_byauthor(source_df):
    '''
    Generates a list of tuples with information for all manuscripts in the database.
    It includes information about a single author, keywords and abstract. For each
    manuscript there are n entries depending on the number of authors.

    Returns
    -------
    list : A list of tuples with three strings each.
    '''
    
    data = []
    for row in range(len(source_df)):
        authors = source_df.iloc[row, 2].split(', ')
        for author in authors:
            keywords = source_df.iloc[row, 3]
            abstract = source_df.iloc[row, 7]
            title = source_df.iloc[row, 1]
            ms_id = source_df.iloc[row, 0]
            datapoint = (author, keywords, abstract, title, ms_id)
            data.append(datapoint)
    return data

#%%

def generate_manuscripts(source_df):
      
    manuscripts_df = pd.DataFrame(ms_byauthor(source_df), columns = ['Author', 'Keywords', 'Abstract', 'Title', 'Id'])

    manuscripts_df = drop_authors(manuscripts_df, 2)

    print()
    print('Lemmatizing keywords...')
    # This lemmatizes the keywords
    manuscripts_df['Keywords'] = manuscripts_df['Keywords'].apply(lemmatize_keywords)
    
    # Generate n-gram dictionary and a column of n-gram keywords in manuscripts_df
    get_ngrams2(manuscripts_df)

    # Before replacing th n-grams in the abstract, it is necessary to lemmatize the abstracts
    print()
    print('Lemmatizing abstracts...')
    manuscripts_df['Abstract'] = manuscripts_df['Abstract'].apply(lemmatize_abstract)
    
    print()
    print('Replacing n-grams in abstracts...')
    print('This might take a while.')
    manuscripts_df['Abstract'] = manuscripts_df['Abstract'].apply(replace_ngrams)
    
    manuscripts_df.to_csv('manuscripts.csv', index=False)
    
    return manuscripts_df


#%%

#############################
# This is for authors_df
#############################

def authors(df):
    
    print()
    print('Combining abstracts and keywords...')
    
    # This takes a df and generates a tuple with an author's name, their keywords and abstracts
    info = combine_abstracts_keywords(df)
    
    # This generates a df with the tuple and names its columns
    authors_df = pd.DataFrame(info, columns=['Author', 'Keywords', 'Abstracts'])

    #Here, the list of keywords become a string
    authors_df['Keywords'] = authors_df['Keywords'].apply(lambda x: ', '.join([i for lista in x for i in lista]))
    
    #Here, the list of abstracts become a string
    authors_df['Abstracts'] = authors_df['Abstracts'].apply(lambda x: '. '.join([i for i in x]))
    
    # This lemmatizes the nouns in the abstract
    #authors_df['Abstracts'] = authors_df['Abstracts'].apply(clean_abstract)
    
    # This combines keywords and abstracts into the abstracts column
    authors_df['Abstracts'] = authors_df['Keywords'] + authors_df['Abstracts']
    
    # This generates a csv file
    authors_df.to_csv('authors_df.csv', index=False)
    
    return authors_df

#%%

def generate_dfs(source_df):
    
    manuscripts = generate_manuscripts(source_df)
    authors_df = authors(manuscripts)
    
    return manuscripts, authors_df

#%%
print()
enter_year = input("Would you like to set a custom start year for selecting abstracts? If you do, type 'y'. Otherwise, press Enter to continue with a year by default (2016). ")
if enter_year.lower() == 'y':
    year = input('Enter the year from which you would like to consider abstracts. ')
else:
    year = 2016

print()
enter_csv = input("Would you like to use new data from Lingbuzz? If you do, type 'y'. Otherwise, press Enter to continue with the provided data (lingbuzz_002_007537.csv). ")
if enter_csv.lower() == 'y':
    file = input('Enter the name of the csv file you want to use. ')
else:
    file = 'lingbuzz_002_007537.csv'


# Load the data from lingbuzz
source_df = pd.read_csv(file)

# Drop nan entries
source_df.dropna(subset=['Title'], inplace=True)

# Filling the empty abstract spaces with empty strings
source_df['Abstract'] = source_df['Abstract'].fillna('')

# Combining the text in titles and abstracts
source_df['Abstract'] = source_df['Title'] + '. ' + source_df['Abstract']

# Giving format to the Date column and droping manuscripts older than 2016
source_df['Date'] = pd.to_datetime(source_df['Date'])
source_df = source_df[source_df['Date'].dt.year >= year]
source_df['Date'] = source_df['Date'].dt.strftime('%Y')


generate_dfs(source_df)