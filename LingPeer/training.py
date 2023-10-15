import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib


#########################
# This is the first classifier: naive bayes over authors
#########################

df1 = pd.read_csv('authors_df.csv')


# This instantiates the TF-IDF vectorizer
vectorizer1 = CountVectorizer(
    max_features=2500,
    stop_words='english',
    lowercase=True
    )

#This fits and transform the abstracts
X_features1 = vectorizer1.fit_transform(df1['Abstracts'])

# This defines the label
y1 = df1['Author']

# The following three lines (i) instantiate the naive Bayes classifier, (ii) train it and (iii) make test predictions
classifier1 = MultinomialNB()
classifier1.fit(X_features1, y1)


#This saves the naive Bayes classifier.
file1 = 'classifier1.pkl'
joblib.dump(classifier1, file1)


#This creates and saves a count vectorization of the abstracts
#c_vect1 = CountVectorizer(lowercase=True, stop_words='english', max_features=2500)
#c_vect1.fit_transform(df1['Abstracts'])
#joblib.dump(c_vect1, 'c_vect1.pkl')

# This is a test. should be erased if it doesn't work
joblib.dump(vectorizer1, 'c_vect1.pkl')


#%%
# This generates a dictionary with authors as keys and their keywords as values

keyword_dict = {}

for index, row in df1.iterrows():
    author = row['Author']
    keywords = row['Keywords']
    
    keyword_dict[author] = keywords

joblib.dump(keyword_dict, 'kw_dict.pkl')




#%%
#########################
# This is the second classifier: naive bayes over individual abstracts
#########################

df2 = pd.read_csv('manuscripts.csv')

df2 = df2.dropna(subset=['Abstract'])
#%%

vectorizer2 = CountVectorizer(
        max_features=800,
        stop_words='english',
        lowercase=True
    )
 
  
#This fits and transform the abstracts
X_features2 = vectorizer2.fit_transform(df2['Abstract'])

# This defines the labels
y2 = df2['Author']

# The following three lines (i) instantiate the naive Bayes classifier and (ii) trains it
classifier2 = MultinomialNB()
classifier2.fit(X_features2, y2)

#This saves the naive Bayes classifier.
file2 = 'classifier2.pkl'
joblib.dump(classifier2, file2)

#c_vect2 = CountVectorizer(lowercase=True, stop_words='english', max_features=800)
#c_vect2.fit_transform(df2['Abstract'])
#joblib.dump(c_vect2, 'c_vect2.pkl')

# Test
joblib.dump(vectorizer2, 'c_vect2.pkl')
joblib.dump(X_features2, 'x2.pkl')

#%%

# vectorizer3 = CountVectorizer(
#     max_features=800,
#     stop_words='english',
#     lowercase=True
#     )

# #This fits and transform the abstracts
# X_features3 = vectorizer3.fit_transform(df2['Abstract'])

# #This creates and saves a count vectorization of the abstracts
# joblib.dump(vectorizer3, 'c_vect3.pkl')
