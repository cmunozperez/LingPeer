import spacy
import re
import os
import joblib
#from generate_dfs import get_ngrams
nlp = spacy.load('en_core_web_lg')

path = os.path.dirname(__file__)

def clean_abstract(string_of_text):
    
    '''
    This function simply changes plural nouns into singular nouns
    '''
    
    a1 = nlp(string_of_text)
    a1_clean = ' '.join([token.lemma_ if token.pos_ == 'NOUN' else token.text for token in a1 if not token.is_punct])
    return a1_clean


def lemmatize_abstract(string_of_text):
    
    a1 = nlp(string_of_text)
    a1_lemma = ' '.join([token.lemma_ for token in a1 if not token.is_punct])

    return a1_lemma


def replace_ngrams(cell):
    
    '''
    This replaces the n-gram keywords in the abstract.
    '''

    for ngram, dummy_token in n_gram_dict.items():
        # This finds the ngrams in the text
        pattern = r'\b' + re.escape(ngram) + r'\b'
        # And this replaces the ngrams with a token
        cell = re.sub(pattern, dummy_token, cell, flags=re.IGNORECASE)

    return cell

#%%

def clean_keywords(string_of_text):
    pattern = r', |,|; |;'

    keyword_list = re.split(pattern, string_of_text.lower())
    lemma_list = []
    
    for kw in keyword_list:
        target = nlp(kw)
        lemma_kw = " ".join([token.lemma_ if token.pos_ == 'NOUN' else token.text for token in target])
        lemma_kw = lemma_kw.strip()
        lemma_list.append(lemma_kw)

    lemmatized_keywords = ", ".join(lemma_list)
    return lemmatized_keywords


def lemmatize_keywords(string_of_text):
    '''
    A function that takes a string of terms separated by commas and returns a string of lemmatized words separated by commas.

    Parameters
    ----------
    string_of_text (str): Some keywords to lemmatize

    Returns
    -------
    A String (str)

    '''
    pattern = r', |,|; |;'

    keyword_list = re.split(pattern, string_of_text.lower())
    lemma_list = []
    
    for kw in keyword_list:
        target = nlp(kw)
        lemma_kw = " ".join([token.lemma_ for token in target if not token.is_punct])
        lemma_kw = lemma_kw.strip()
        lemma_list.append(lemma_kw)

    lemmatized_keywords = ", ".join(lemma_list)
    return lemmatized_keywords

try:
    n_gram_dict = joblib.load(path + '/n_grams.pkl')
except:
    print('N-gram dictionary not found.')

