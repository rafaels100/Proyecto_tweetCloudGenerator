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

def limpiarTexto(text):
    #paso a minusculas
    text = text.lower()
    #busco por links y los remuevo
    pattern = re.compile(r"https://[a-zA-Z0-9./]+")
    text = re.sub(pattern, " ", text)
    #elimino puntos suspensivos
    pattern = re.compile(r"(\.\.\.)")
    text = re.sub(pattern, " ", text)
    #busco mas de dos espacios en blanco y los reemplazo por uno solo
    pattern = re.compile(r"\s+")
    text = re.sub(pattern, " ", text)
    return text

def eliminarStopWords(text):
    #copiar codigo de tp
    #voy a querer eliminar las stop words
    stopword_es = nltk.corpus.stopwords.words('spanish')
    text = " ".join([word for word in text.split(" ") if word not in stopword_es])
    return text


def lematizarYquitarStopWords(text):
    print("lematizar o no lematizar? Esa es la cuestion.")
    #copiar codigo de tp
    #se puede lematizar palabras en español ?
    #Si no se puede, usar tweets en ingles, como los de Federer o Stan the Man

def wordCloud_palabras(text_tweets, user_name, guardadoNoguardado):
    #--------------------EXTRAYENDO PALABRAS-------------------------------
    #extrayendo todas las palabras usadas por el usuario
    #instancio el objeto wordcloud. Como ya eliminamos las stopwords, ponemos None
    wordcloud_palabras = WordCloud(width = 1000, height = 1000, random_state=1,
                                   collocations=False, stopwords=None).generate(text_tweets)

    #ploteo la wordcloud
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title(f"Palabras mas usadas del usuario {user_name}")
    ax.imshow(wordcloud_palabras)
    ax.set_axis_off()
    if guardadoNoguardado == 2:
        plt.savefig(f"wordcloud_palabras_{user_name}.png")
    plt.show()

def wordCloud_emojis(text_tweets, user_name, guardadoNoguardado):
    #----------------------EXTRAYENDO EMOJIS---------------------
    #Creo un patron para extraer los emojis, que tienen la forma :emoji:, dada por
    #la libreria emoji.
    pattern = re.compile(r":[a-zA-Z_]+:")
    #creo una string larga con todos los matches
##    emojis_str = " ".join([" ".join([match.group(0) for match in pattern.finditer(text)])
##                           for text in text_tweets if sum(1 for match in pattern.finditer(text)) != 0])
    emojis_matches = pattern.finditer(text_tweets)
    #print(emojis_matches)
    emojis_str = " ".join([match.group(0) for match in emojis_matches])
    #print("EMOJIS: ", emojis_str)
    #instancio el objeto wordcloud. Como ya eliminamos las stopwords, ponemos None
    wordcloud_emojis = WordCloud(width = 1000, height = 1000, random_state=1,
                                 collocations=False, stopwords=None).generate(emojis_str)

    #ploteo la wordcloud
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title(f"Emojis mas usados del usuario {user_name}")
    ax.imshow(wordcloud_emojis)
    ax.set_axis_off()
    if guardadoNoguardado == 2:
        plt.savefig(f"wordcloud_emojis_{user_name}.png")
    plt.show()

def wordCloud_hashtags(text_tweets, user_name, guardadoNoguardado):
    #----------------------EXTRAYENDO HASHTAGS---------------------
    #Los hashtags empiezan con #
    #Hashtags can only contain letters, numbers, and underscores (_),
    #no special characters. Only 30 hashtags are allowed in each post
    pattern = re.compile(r"#[a-zA-Z0-9_]+")
    #creo una string larga con todos los matches    
##    hash_str = " ".join([" ".join([match.group(0) for match in pattern.finditer(text)])
##                           for text in text_tweets if sum(1 for match in pattern.finditer(text)) != 0])
    hash_matches = pattern.finditer(text_tweets)
    print(hash_matches)
    hash_str = " ".join([match.group(0) for match in hash_matches])
    #instancio el objeto wordcloud. Como ya eliminamos las stopwords, ponemos None
    print("HASHTAGS: ", hash_str)
    wordcloud_hash = WordCloud(width = 1000, height = 1000, random_state=1,
                                 collocations=False, stopwords=None).generate(hash_str)
    #ploteo la wordcloud
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title(f"Hashtags mas usados del usuario {user_name}")
    ax.imshow(wordcloud_hash)
    ax.set_axis_off()
    if guardadoNoguardado == 2:
        plt.savefig(f"wordcloud_hashtags_{user_name}.png")
    plt.show()
    
    

def tweetcloud(usuario, tipoWordcloud, guardadoNoguardado):
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
    user_name = usuario
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
    #print(text_tweets)
    #convierto todo a una sola string
    str_tweets = " ".join(text_tweets)
    #limpio las palabras 
    str_tweets_clean = limpiarTexto(str_tweets)
    #print("-----------CLEAN---------------")
    #print(str_tweets_clean)
    #quito stopwords
    str_tweets_sinSW = eliminarStopWords(str_tweets_clean)
    #¿y lematizo? Tal vez no sea una buena idea, si quiero capturar cosas como emojis en mis
    #wordclouds. Creo que deberia limitarme a eliminar stopwords
##    str_tweets_lemma = lematizar(str_tweets_sinSW)
    #segun el tipo de wordcloud seleccionado por el usuario,
    #accedo a la funcion adecuada
    if tipoWordcloud == "Palabras":
        wordCloud_palabras(str_tweets_sinSW, user_name, guardadoNoguardado)
    elif tipoWordcloud == "Hashtags":
        wordCloud_hashtags(str_tweets_sinSW, user_name, guardadoNoguardado)
    else:
        wordCloud_emojis(str_tweets_sinSW, user_name, guardadoNoguardado)


