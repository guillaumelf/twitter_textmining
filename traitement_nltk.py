
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 14:23:47 2017

@author: Guillaume
"""

### Import de librairies
########################

from nltk.tokenize import TweetTokenizer, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor

### Définition locale de fonctions
##################################

def tokenize_stopwords(texte):
    mots = tokenizer_mots.tokenize(texte)
    lst = [m.lower() for m in mots if m.lower() not in stop_words and m.lower().startswith('#') == False] # elimination des mots vides et des hashtags
    return lst   

list_allowed = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','£','€','0','1','2','3','4','5','6','7','8','9','10']
def remove_useless(word):
    useful = 0
    letters = list(word)
    for elem in list_allowed :
        if elem in letters :
            useful +=1
    if useful == 0 :
        new_word = 'useless'
    else :
        new_word = word
    return new_word
                  
### Import des données et pré-traitement
########################################

wenger = list(pd.read_csv('wenger.csv',sep=';',header=0,decimal='.',encoding='utf-8').text)
mourinho = list(pd.read_csv('mourinho.csv',sep=';',header=0,decimal='.',encoding='utf-8').text)

# On enlève les "RT @blablabla:" à l'aide d'une expression régulière ainsi que les '\n'

regex = re.compile(r'[\n\r\t]')
wenger = [re.sub(r"RT @(.*?):",r"",tweet) for tweet in wenger]
wenger = [re.sub(r"RT",r"",tweet) for tweet in wenger]
wenger = [re.sub(r"è",r"e",tweet) for tweet in wenger]
wenger = [regex.sub(' ',tweet) for tweet in wenger]
mourinho = [re.sub(r"RT @(.*?):",r"",tweet) for tweet in mourinho]
mourinho = [re.sub(r"RT",r"",tweet) for tweet in mourinho]
mourinho = [re.sub(r"é",r"e",tweet) for tweet in mourinho]
mourinho = [regex.sub(' ',tweet) for tweet in mourinho]


# Tokenisation 1ere étape : on enlève les noms d'utilisateurs et autres @ et on regroupe en un seul paragraphe

tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
paragraph_wenger = ' '.join(map(lambda tweet : ' '.join(tweet),list(map(lambda tweet : tokenizer.tokenize(tweet),wenger))))
paragraph_mourinho = ' '.join(map(lambda tweet : ' '.join(tweet),list(map(lambda tweet : tokenizer.tokenize(tweet),mourinho))))

# Tokenisation 2eme étape : on extrait les mots en éliminant les mots vides

tokenizer_mots = RegexpTokenizer('[\s+\'\.\,\?\!();\:\"\[\]\|\&]',gaps=True)
stop_words = set(stopwords.words())
new_words = ['like','must','us','got','even','still','via'] # ajout de mots à cette liste de mots vides
for word in new_words :
    stop_words.add(word) 
e = ThreadPoolExecutor() # Utilisation de tous les coeurs de la machine pour baisser le temps de calcul
wenger_words = e.map(remove_useless,tokenize_stopwords(paragraph_wenger))
wenger_words = [word for word in wenger_words if word != 'useless'] #Supression des caractères non-éliminés par la regex
mourinho_words = e.map(remove_useless,tokenize_stopwords(paragraph_mourinho))
mourinho_words = [word for word in mourinho_words if word != 'useless']

# Premier calcul de fréquences  : affichage à l'écran + écriture dans un fichier

file = open('wenger_words.txt','w')
fdist = FreqDist(word.lower() for word in wenger_words)
most_common = fdist.most_common(300)
most_common.pop(0) # supression du nom et du prénom du manager
most_common.pop(0)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])
        file.write("{}:{}\n".format(most_common[i][0],most_common[i][1]))
file.close()
print('#################################################')
file = open('mourinho_words.txt','w')
fdist = FreqDist(word.lower() for word in mourinho_words)
most_common = fdist.most_common(300)
most_common.pop(0)
most_common.pop(0)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])
        file.write("{}:{}\n".format(most_common[i][0],most_common[i][1]))
file.close()
print('#################################################')

# Racinisation

stemmer = PorterStemmer()
stem_wenger = list(map(lambda word : stemmer.stem(word),wenger_words))
stem_mourinho = list(map(lambda word : stemmer.stem(word),mourinho_words))

# Lemmatisation

lemmatizer = WordNetLemmatizer()
lemme_wenger = list(map(lambda word : lemmatizer.lemmatize(word,pos="v"),stem_wenger))
lemme_mourinho = list(map(lambda word : lemmatizer.lemmatize(word,pos="v"),stem_mourinho))

# Second calcul de fréquences 

file = open('wenger_stems.txt','w')
fdist = FreqDist(word.lower() for word in lemme_wenger)
most_common = fdist.most_common(300)
most_common.pop(0)
most_common.pop(0)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])
        file.write("{}:{}\n".format(most_common[i][0],most_common[i][1]))
file.close()
print('#################################################')
file = open('mourinho_stems.txt','w')
fdist = FreqDist(word.lower() for word in lemme_mourinho)
most_common = fdist.most_common(300)
most_common.pop(0)
most_common.pop(0)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])
        file.write("{}:{}\n".format(most_common[i][0],most_common[i][1]))
file.close()