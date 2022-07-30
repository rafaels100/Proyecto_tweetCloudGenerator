from tweepy import API
from tweepy.auth import OAuthHandler
import json
import pandas as pd
import emoji
import re
import string
from wordcloud import WordCloud
import nltk
import matplotlib.pyplot as plt

#---------------------ACCEDIENDO A API TWITTER---------------------------
#Pasamos credenciales a la api para conectarnos
api_key = "ec9kgP7ZZfzR6OvOxdidqhkxY"
api_key_secret = "72zuYB8uVgkvE0FfjILK5pqwZHrkE994MUCK4qlBdDh3GelTxd"
access_token = "1542218199470686209-d3Ymd8mZc7clCwa6sQEKSCZT0DKkRh"
access_token_secret = "Z1AjNhu9I6VFm5CJd6lMcicFMkHJemBa91N9VwOh9PqN6"
auth = OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

#elegimos el usuario
user_name = "andreasonard"
#fetcheo los tweets del usuario. Puedo pedir hasta los ultimos 200 tweets
tweets = api.user_timeline(screen_name=user_name, count=200, include_rts=False,
                           tweet_mode="extended")
print(f"Cantidad de tweets {len(tweets)}")

#creo una lista con los textos de los tweets
text_tweets = [tweet.full_text for tweet in tweets]

#los emojis traen problemas a la hora de imprimir los tweets. Podemos usar
#la libreria emoji para convertir los emojis a sus sentimientos, en vez
#del emoji en si.
text_tweets = [emoji.demojize(text) for text in text_tweets]
print(text_tweets)

#--------------------EXTRAYENDO PALABRAS-------------------------------
#extrayendo todas las palabras usadas por el usuario
##print(text_tweets)

str_tweets = " ".join(text_tweets)

def limpiarTexto(text):
    #paso a minusculas
    text = text.lower()
    #busco por links y los remuevo
    pattern = re.compile(r"https://[a-zA-Z0-9./]+")
    text = re.sub(pattern, " ", text)
    #elimino puntos suspensivos
    pattern = re.compile(r"(\.\.\.)")
    text = re.sub(pattern, " ", text)
    #busco mas de dos espacios en blanco
    pattern = re.compile(r"\s+")
    text = re.sub(pattern, " ", text)
    return text

print(str_tweets)
str_tweets_clean = limpiarTexto(str_tweets)
print("------------------CLEAN------")
print(str_tweets_clean)

#---------------------WORDCLOUD----------------------

stopword_es = nltk.corpus.stopwords.words('spanish')
#instancio el objeto wordcloud
wordcloud_emojis = WordCloud(width = 1000, height = 1000, random_state=1,
                             collocations=False, stopwords=stopword_es).generate(str_tweets_clean)

#ploteo las wordclouds
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_title(f"Palabras mas usadas del usuario {user_name}")
ax.imshow(wordcloud_emojis)
ax.set_axis_off()
#plt.savefig(f"wordcloud_emojis_{user_name}.png")
plt.show()

