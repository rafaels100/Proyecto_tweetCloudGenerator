from tweepy import API
from tweepy.auth import OAuthHandler
import json
import pandas as pd
import emoji
import re
from wordcloud import WordCloud
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

str_larga = " ".join(text_tweets)
print(str_larga)

#---------------------WORDCLOUD----------------------


#instancio el objeto wordcloud
wordcloud_emojis = WordCloud(width = 1000, height = 1000, random_state=1,
                             collocations=False, stopwords=None).generate(str_larga)

#ploteo las wordclouds
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_title(f"Emojis mas usados del usuario {user_name}")
ax.imshow(wordcloud_emojis)
ax.set_axis_off()
plt.savefig(f"wordcloud_emojis_{user_name}.png")
plt.show()


#------------------------PARSEANDO LOS TWEETS-----------------------------
#Con regex, podemos parsear los tweets, extrayendo la info deseada.

#Creo un patron para extraer los emojis, que tienen la forma :emoji:, dada por
#la libreria emoji.
pattern = re.compile(r":[a-zA-Z_]+:")

#puedo crear una lista con los objetos matches para cada tweet
matches = [[match for match in pattern.finditer(text)] for text in text_tweets]
#print(matches)

#puedo tambien acceder directamente a la string de matcheo, en vez de quedarme
#con el objeto match
emojis = [[match.group(0) for match in pattern.finditer(text)] for text in text_tweets]
##print(emojis)

#vemos que hay varias listas vacias, correspondientes a las veces en que no
#hubo matcheo. Podemos evitar esto pidiendo que solo consideremos a aquellos
#tweets en los que hubo al menos un matcheo
emojis_1 = [[match.group(0) for match in pattern.finditer(text)] for text in text_tweets if sum(1 for match in pattern.finditer(text)) != 0]
##print(emojis_1)

#podemos ahora llevar esta lista de listas de strings a una sola string
emojis_1_str = emojisStr = " ".join([" ".join(lista) for lista in emojis_1])
##print(emojis_1_str)

#incluso podriamos haberlo hecho de la lista de emojis que todavia contenia
#listas vacias, de este modo:
emojis_str = " ".join([" ".join(lista) for lista in emojis if lista != []])
##print(emojis_str)

#podemos combinar todos estos approach y conseguir una string con todos los
#emojis directamente, sin necesidad de conseguir primero una lista de listas
#de emojis:
emojis_str_final = " ".join([" ".join([match.group(0) for match in pattern.finditer(text)])
                             for text in text_tweets if sum(1 for match in pattern.finditer(text)) != 0])
##print(emojis_str_final)



#-----------------------------WORDCLOUD DE EMOJIS--------------------------------
#Teniendo una string con todos los emojis, puedo hacer una wordcloud para ver
#cuales son los emojis mas usados por el usuario.

#primero, limpio un poco los emojis
##pattern = re.compile(r":")
##
##emojis_wc = pattern.sub("", emojis_str_final)
####print(emojis_wc)
##
###instancio el objeto wordcloud
##wordcloud_emojis = WordCloud(width = 1000, height = 1000, random_state=1,
##                             collocations=False, stopwords=None).generate(emojis_wc)
##
###ploteo las wordclouds
##fig, ax = plt.subplots(figsize=(10, 10))
##ax.set_title(f"Emojis mas usados del usuario {user_name}")
##ax.imshow(wordcloud_emojis)
##ax.set_axis_off()
##plt.savefig(f"wordcloud_emojis_{user_name}.png")
##plt.show()




#-----------------------------EXTRAYENDO HASHTAGS---------------------------
"""
Los hashtags empiezan con #
Hashtags can only contain letters, numbers, and underscores (_),
no special characters. Only 30 hashtags are allowed in each post
"""
##print("hashtags")
pattern = re.compile(r"#[a-zA-Z0-9_]+")
hastag_str_final = " ".join([" ".join([match.group(0) for match in pattern.finditer(text)])
                             for text in text_tweets if sum(1 for match in pattern.finditer(text)) != 0])
##print(hastag_str_final)


#-----------------------------WORDCLOUD HASHTAGS------------------------------
#instancio el objeto wordcloud
wordcloud_hashtags = WordCloud(width = 1000, height = 1000, random_state=1,
                               collocations=False, stopwords=None).generate(hastag_str_final)

#ploteo las wordclouds
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_title(f"Hashtags mas usados del usuario {user_name}")
ax.imshow(wordcloud_hashtags)
ax.set_axis_off()
#plt.savefig(f"wordcloud_hashtags_{user_name}.png")
plt.show()


#-----------------------------EXTRAYENDO LINKS--------------------------------
#los links empiezan con https:// y pueden tener letras, puntos, /, pero no ' ni ,.
##print("links")
pattern = re.compile(r"https?://[a-zA-Z0-p./]+")
links_str_final = " ".join([" ".join([match.group(0) for match in pattern.finditer(text)])
                            for text in text_tweets if sum(1 for match in pattern.finditer(text)) != 0])
##print(links_str_final)


#------------------------------WORDCLOUDS DE LINKS------------------
#instancio el objeto wordcloud
##wordcloud_hashtags = WordCloud(width = 1000, height = 1000, random_state=1,
##                               collocations=False, stopwords=None).generate(links_str_final)
##
###ploteo las wordclouds
##fig, ax = plt.subplots(figsize=(10, 10))
##ax.set_title(f"Links mas usados del usuario {user_name}")
##ax.imshow(wordcloud_hashtags)
##ax.set_axis_off()
###plt.savefig(f"wordcloud_hashtags_{user_name}.png")
##plt.show()
