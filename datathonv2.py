# -*- coding: utf-8 -*-
"""Datathonv2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zpbGjrd_ZwQOp73zyQYKm_M0R1lob7Ba
"""

!pip install -q tweepy matplotlib wordcloud

import pandas as pd
archivo_excel = pd.read_csv('Dathaton.csv')
tweets = archivo_excel['tweet'].values

## Importación de Librerías
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import torch
import json  ## Importamos la librería para trabajar con JSON

## Declaración de Funciones

def predict_sentiment(text, model, tokenizer, label_encoder, device):
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    predicted_class = torch.argmax(outputs.logits, dim=1)
    return label_encoder.inverse_transform(predicted_class.cpu())[0]

## Iniciamos el Modelo

tokenizer = BertTokenizer.from_pretrained("ignacio-ave/BETO-nlp-sentiment-analysis-spanish")
model = BertForSequenceClassification.from_pretrained("ignacio-ave/BETO-nlp-sentiment-analysis-spanish")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

label_encoder = LabelEncoder().fit(['P+', 'P', 'NEU', 'NONE', 'N', 'N+'])

results_multiple = []

for tweet in tweets:
    prediction = predict_sentiment(tweet, model, tokenizer, label_encoder, device)
    results_multiple.append({
        "Tweet": tweet,
        "Predicción": prediction
    })

import pandas as pd

## Cargamos la información en un dataframe
pd.set_option('max_colwidth', None)
pd.set_option('display.width', 3000)
df = pd.DataFrame(results_multiple)

import matplotlib.pyplot as plt

## Contamos la frecuencia de tweets por sentimiento
sentiment_counts = df.groupby(['Predicción']).size()
print(sentiment_counts)

## Manejamos los sentimientos de cada tweet
fig = plt.figure(figsize=(6,6), dpi=100)
ax = plt.subplot(111)
sentiment_counts.plot.pie(ax=ax, autopct='%1.1f%%', startangle=270, fontsize=12, label="")

from wordcloud import WordCloud
from wordcloud import STOPWORDS

## Creamos un Wordcloud con las palabras positivas más repetidas
positive_tweets = df['Tweet'][df["Predicción"] == 'P+']
stop_words = ["https", "co", "RT", "la", "en", "que", "de", "una", "un", "los", "y", "lo", "mi", "te", "Muchas", "gracias", "excelente", "muchisimas", "saludos", "estimados", "al", "del", "object", "name","dtype" ] + list(STOPWORDS)
positive_wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white", stopwords = stop_words).generate(str(positive_tweets))
plt.figure()
plt.title("Tweets Positivos+ - Wordcloud")
plt.imshow(positive_wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
