#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:13:40 2018

@author: chenhuizhang
"""
import os
import gensim as ge
import nltk
import re
import string as st
import pandas as pd
from nltk.corpus import stopwords

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

doc = df['Review']

def text_parsing (doc):
    """
    input: doc is a list/series in which each element is a piece of text in English.
    output: a list in which each piece of text has been parsed as a list of words.
    The text parsing involves removing punctuations, stop words and stemming.
    """
    import re
    from nltk.corpus import stopwords
    import nltk
    
    # Remove punctuation, then tokenize documents
    
    punc = re.compile( '[%s]' % re.escape( string.punctuation ) )
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
df.head()



