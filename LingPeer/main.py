#import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from clean_text import lemmatize_keywords, replace_ngrams, lemmatize_abstract
import joblib
import re
import argparse
import os
#import re

####################################
####################################

def preprocess(title, keywords, abstract):
    # This combines the strings in the title and the abstract
    abstract = title + '. ' + abstract
     
    abstract = lemmatize_abstract(abstract)
    
    abstract = replace_ngrams(abstract)
     
    # This decapitalizes all words in the abstract
    abstract = ' '.join([word.lower() for word in abstract.split(' ')])

    keywords = lemmatize_keywords(keywords)
    ngram_kws = []
    for kw in keywords.split(', '):
        if kw in n_gram_dict.keys():
            ngram_kws.append(n_gram_dict[kw])
        else:
            ngram_kws.append(kw)
    ngram_kws = ', '.join(ngram_kws)
    
    abstract_kws = ngram_kws + '. ' + abstract
    
    return (abstract, abstract_kws, ngram_kws)
    

def model1(abstract):
    # This vectorizes the provided abstract
    abstract_vect = c_vect1.transform([abstract])

    # This gets the probabilities for each of the authors in the database
    pred_proba = classifier1.predict_proba(abstract_vect.reshape(1, -1))

    class_labels = classifier1.classes_

    class_labels = [str(i) for i in class_labels]

    # This combines the probabilities with each of the authors
    class_probabilities = [(label, prob) for label, prob in zip(class_labels, pred_proba[0])]

    # Sort class probabilities in descending order
    class_probabilities.sort(key=lambda x: x[1], reverse=True)
    
    return class_probabilities
    
def model2(abstract):
     
    # This vectorizes the provided abstract
    abstract_vect = c_vect2.transform([abstract])

    # This gets the probabilities for each of the authors in the database
    pred_proba = classifier2.predict_proba(abstract_vect.reshape(1, -1))

    class_labels = classifier2.classes_

    class_labels = [str(i) for i in class_labels]

    # This combines the probabilities with each of the authors
    class_probabilities = [(label, prob) for label, prob in zip(class_labels, pred_proba[0])]

     # Sort class probabilities in descending order
    class_probabilities.sort(key=lambda x: x[1], reverse=True)
     
    return class_probabilities           
  

#################################################
#%%

def kw_comparer(ngram_kws):
    '''
    Takes a string with keywords (with n-grams) and return a list of authors who
    have used at least half of those keywords.

    Parameters
    ----------
    ngram_kws (str) : a string with keywords 

    Returns
    -------
    author_same_kws (list): a list of authors
    
    '''
    
    author_same_kws = []
    #list_kws = []
    ngram_kws = ngram_kws.split(', ')
    len_kws = len(ngram_kws)
    ngram_kws = set(ngram_kws)
    for author, kws in kw_dict.items():
        kws = set(kws.split(', '))
        intersection = kws & ngram_kws
        if len(intersection) > 2 and len(intersection) > (len_kws/2):
            author_same_kws.append(author)
            #list_kws.append(list(intersection))
    return author_same_kws #, list_kws)

#%%
def get_matching_keywords(author_list, ngram_kws, keywords):
    kws_for_authors = []
    ngram_kws = ngram_kws.split(', ')
    order_kws = ngram_kws.copy() 
    ngram_kws = set(ngram_kws)
    pattern = r', |,|; |;'
    keywords = re.split(pattern, keywords)
    
    for author in author_list:
        #print(ngram_kws)
        all_kws = kw_dict[author]
        all_kws = set(all_kws.split(', '))
        #print(all_kws)
        intersection = list(all_kws & ngram_kws)
        orig_kws = []
        for word in intersection:
            orig_kw = keywords[order_kws.index(word)]
            orig_kws.append(orig_kw)
        #print(len(intersection))
        #print('----')
        kws_for_authors.append(orig_kws)
    
    return kws_for_authors

#%%

def get_peers(title, keywords, abstract):

    preprocessed = preprocess(title, keywords, abstract)
    
    model_A = model1(preprocessed[1])
    
    model_B = model2(preprocessed[0])
    
    authors_kws = kw_comparer(preprocessed[1])
    
    filter_first_a = set([]) #set([model_A[0][0]])
    
    filter_one_percent_a = set([name for name, score in model_A if score > 0.01])
    
    filter_first_b = set([]) #set([model_B[0][0]])
    
    filter_one_percent_b = set([name for name, score in model_B if score > 0.01])
    
    filter_two_mods = set([name for name, score in model_A if score > 0.001]) & set([name for name, score in model_B if score > 0.001])
    
    if len(authors_kws) > 0:
        filter_kws = set([name for name, score in model_A if score > 0.001]) & set(authors_kws[0])
    else:
        filter_kws = set([])
    
    final_list = list(filter_first_a | filter_one_percent_a | filter_first_b | filter_one_percent_b |filter_two_mods | filter_kws)
    
    # This is to get the id of the most relevant paper for each author.
    # First, we get a vector for the provided abstract
    abstract_vect = c_vect2.transform([preprocessed[0]])
    
    # Now we calculate cosine similarity
    
    cosine_sims = cosine_similarity(abstract_vect, x2)
    
    cosine_sims = pd.DataFrame(cosine_sims).T
    cosine_sims = cosine_sims.rename(columns={0: 'Cosine_sim'})
    
    cosine_sims[['Author', 'Title', 'Id']] = manuscripts[['Author', 'Title', 'Id']].copy()
    
    titles = []
    
    ids = []
    
    cos_sims = []
    
    for author in final_list:
        filtered_df = cosine_sims[cosine_sims['Author'] == author]
        max_index = filtered_df['Cosine_sim'].idxmax()
        author_cs = filtered_df.at[max_index, 'Cosine_sim']
        author_title = filtered_df.at[max_index, 'Title']
        author_id = filtered_df.at[max_index, 'Id']
        cos_sims.append(author_cs)
        titles.append(author_title)
        ids.append(author_id)
    
    matching_kws = get_matching_keywords(final_list, preprocessed[2], keywords)
    
    authors_and_info = sorted(list(zip(final_list, matching_kws, titles, ids, cos_sims)), reverse=True, key=lambda x: len(x[1]))      
    return authors_and_info


#%%

# The following gives the option of generating new training data in case you want to use more current abstracts from Lingbuzz
parser = argparse.ArgumentParser(description='An app that gets potential reviewers for abstracts in theoretical linguistics based on data from Lingbuzz')
parser.add_argument('-newdata', action='store_true', help='Allows to change the training data set by providing new Lingbuzz data.')
args = parser.parse_args()

if args.newdata:
    try:
        import preprocessing
        import training
    except:
        print('Something went wrong.')

path = os.path.dirname(__file__)

# This loads dictionaries to work with keywords
kw_dict = joblib.load(path + '/kw_dict.pkl')
n_gram_dict = joblib.load(path + '/n_grams.pkl')

# This loads the data of the authors
manuscripts = pd.read_csv(path + '/manuscripts.csv')

#The following loads the models and the vectorization of the abstracts
classifier1 = joblib.load(path + '/classifier1.pkl')
classifier2 = joblib.load(path + '/classifier2.pkl')
c_vect1 = joblib.load(path + '/c_vect1.pkl')
c_vect2 = joblib.load(path + '/c_vect2.pkl')
x2 = joblib.load(path + '/x2.pkl')

#%%
# This is the part that asks for the info if the script is not imported
if __name__ == "__main__":
    
    title = input('Copy the title of the paper here: ')
    keywords = input('Copy your keywords here: ')
    abstract = input('Copy your abstract here: ')
    
    result = get_peers(title, keywords, abstract)
    
    print()
    print('The following authors have worked on similar topics:')
    print()
    for name, kw_list, title, ms_id, _ in result:
        kw_toprint = ', '.join(kw_list)
        print(f'\t-{name} has worked on {kw_toprint}. A relevant manuscript to check is "{title}", whose Lingbuzz id is {ms_id}.')
        print()