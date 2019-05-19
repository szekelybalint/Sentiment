#%%
import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
from bs4 import BeautifulSoup
import re
from nltk.tokenize import WordPunctTokenizer

plt.style.use('fivethirtyeight')

# %matplotlib inline
# %config InlineBackend.figure_format = 'retina'

# cols = ['sentiment', 'id', 'date', 'query_string', 'user', 'text']
# df = pd.read_csv("C:/Projects/Sentiment/training_less.csv", header=None, names=cols)

# df.drop(['id','date','query_string','user'],axis=1,inplace=True)
# df['sentiment'] = df['sentiment'].map({0: 0, 4: 1})
tok = WordPunctTokenizer()

pat1 = r'@[A-Za-z0-9]+'
pat2 = r'https?://[A-Za-z0-9./]+'
combined_pat = r'|'.join((pat1, pat2))

def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'html.parser')
    souped = soup.get_text()
    stripped = re.sub(combined_pat, '', souped)
    try:
        clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        clean = stripped
    letters_only = re.sub("[^a-zA-Z]", " ", clean)
    lower_case = letters_only.lower()
    # During the letters_only process two lines above, it has created unnecessay white spaces,
    # I will tokenize and join together to remove unneccessary white spaces
    words = tok.tokenize(lower_case)
    return (" ".join(words)).strip()

# nums = [0, 4000, 6000, 8000, 11844]

# print ("Cleaning and parsing the tweets...\n")
# clean_tweet_texts = []
# for i in range(nums[0],nums[4]):
#     if( (i+1)%500 == 0 ):
#         print ("Tweets %d of %d has been processed" % ( i+1, nums[1] ))                                                                   
#     clean_tweet_texts.append(tweet_cleaner(df['text'][i]))