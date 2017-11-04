# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 17:19:15 2017

@author: Guillaume
"""

### Import de librairies
########################

import json
import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import re

### Définition locale de fonctions
##################################

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

### Import des données
######################

tweets_data_path = 'twitter_data.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
    
print('Nombre de tweets : '+str(len(tweets_data)))

### Traitement des données
##########################

tweets = pd.DataFrame()
e = ThreadPoolExecutor()

tweets['text'] = e.map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = e.map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = e.map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

tweets_by_lang = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')

tweets_by_country = tweets['country'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')

tweets['guardiola'] = tweets['text'].apply(lambda tweet: word_in_text('guardiola', tweet))
tweets['mourinho'] = tweets['text'].apply(lambda tweet: word_in_text('mourinho', tweet))
tweets['conte'] = tweets['text'].apply(lambda tweet: word_in_text('conte', tweet))
tweets['wenger'] = tweets['text'].apply(lambda tweet: word_in_text('wenger', tweet))
tweets['klopp'] = tweets['text'].apply(lambda tweet: word_in_text('klopp', tweet))
tweets['pochettino'] = tweets['text'].apply(lambda tweet: word_in_text('pochettino', tweet))

















