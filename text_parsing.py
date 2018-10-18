#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:13:40 2018

@author: chenhuizhang
"""
import os
import gensim as ge
import string as st
import pandas as pd


os.getcwd()
os.listdir()

# Create initial documents list
df = pd.read_excel("IMDB_Review_data.xlsx")
print(df.head())

print(df['Review'].head())
type(df['Review'].head()) # one column is a pd series
df.shape

# remove rows with missing values in Review column
df = df.dropna(subset=['Review'])
df = df.dropna(subset=['Genre'])
doc = df['Review']

df["Rating"].value_counts()


def text_parsing (doc):
    """
    input: doc is a list/series in which each element is a piece of text in English.
    output: a list in which each piece of text has been parsed as a list of words.
    The text parsing involves removing punctuations, stop words and stemming.
    """
    import re
    from nltk.corpus import stopwords
    import nltk
    import string as st
    
    # Remove punctuation, then tokenize documents
    
    punc = re.compile( '[%s]' % re.escape( st.punctuation ) )
    term_vec = [ ]
    
    for d in doc:
        d = d.lower()
        
        d = punc.sub( '', d )
        #print(d)
        term_vec.append( nltk.word_tokenize( d ) )

    # Remove stop words from term vectors
    
    stop_words = nltk.corpus.stopwords.words( 'english' )
    
    for i in range( 0, len( term_vec ) ):
        term_list = [ ]
        
        for term in term_vec[ i ]:
            if term not in stop_words:
                term_list.append( term )
    
        term_vec[ i ] = term_list
 
    # Porter stem remaining terms
    
    porter = nltk.stem.porter.PorterStemmer()
    
    for i in range( 0, len( term_vec ) ):
        for j in range( 0, len( term_vec[ i ] ) ):
            term_vec[ i ][ j ] = porter.stem( term_vec[ i ][ j ] )

    return term_vec

# Print term vectors with stop words removed
term_parsed = text_parsing(doc)

len(term_parsed)

df["term_parsed"] = term_parsed
#df.head()
#type(df["Genre"][10])


# Convert the rows in string format of genre column to lists.
df["Genre"][1] # every entry is a string enclosed with quotes
import ast
col_genre = []
for x in df["Genre"]:
    try:
        x = ast.literal_eval(x)
        col_genre.append(x)
    except ValueError:
        l = []
        l.append(x)
        col_genre.append(l)
len(col_genre)

df["Genre"] = col_genre

df["Genre"][1] # now it's a list

                                                                                 
# get top 10 genres and make binary variables to identify the genres a review belongs to
# Comedy Drama Horror Action Thriller Romance Sci-Fi Fantasy Adventure Documentary...

genre_dict = {}
for row in df["Genre"]:
    
    for item in row:
        if item not in genre_dict:
            genre_dict[item] = 1
        else:
            genre_dict[item] +=1

genre_dict
len(genre_dict)

type(df["Genre"])

# create dummy variables for all genres and concatenate to make a final dataframe
dummy = pd.get_dummies(df["Genre"].apply(pd.Series).stack(),prefix='g').sum(level=0) 

dummy.shape
df.shape
dummy.tail(10)

df_final = pd.concat([df,dummy], axis=1)
df_final.shape
# double check
len(df_final.loc[df_final["g_Comedy"] == 1])

df_final.to_csv("data_final.csv")
