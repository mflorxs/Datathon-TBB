

import pandas as pd
archivo_excel = pd.read_csv('Dathaton.csv')
tweets = archivo_excel['tweet'].values
print(tweets)

# 1. Importación de Librerías
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import torch
import json  # <-- Importamos la librería para trabajar con JSON

# 2. Declaración de Funciones

def predict_sentiment(text, model, tokenizer, label_encoder, device):
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    predicted_class = torch.argmax(outputs.logits, dim=1)
    return label_encoder.inverse_transform(predicted_class.cpu())[0]

# 3. Inicialización del Modelo

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

print(json.dumps(results_multiple, ensure_ascii=False, indent=4))  # <-- Imprimimos en formato JSON

import pandas as pd

# Load the data in a dataframe
pd.set_option('max_colwidth', None)
pd.set_option('display.width', 3000)
df = pd.DataFrame(results_multiple)

# Show a tweet for each sentiment
display(df[df["Predicción"] == 'P+'].head(1))
display(df[df["Predicción"] == 'P'].head(1))
display(df[df["Predicción"] == 'NEU'].head(1))
display(df[df["Predicción"] == 'NONE'].head(1))
display(df[df["Predicción"] == 'N'].head(1))
display(df[df["Predicción"] == 'N+'].head(1))

import matplotlib.pyplot as plt

# Let's count the number of tweets by sentiments
sentiment_counts = df.groupby(['Predicción']).size()
print(sentiment_counts)

# Let's visualize the sentiments
fig = plt.figure(figsize=(6,6), dpi=100)
ax = plt.subplot(111)
sentiment_counts.plot.pie(ax=ax, autopct='%1.1f%%', startangle=270, fontsize=12, label="")

from wordcloud import WordCloud
from wordcloud import STOPWORDS

# Wordcloud with positive tweets
positive_tweets = df['Tweet'][df["Predicción"] == 'P+']
stop_words = ["https", "co", "RT", "la", "en", "que", "de", "una", "un", "los", "y", "lo", "mi", "te" ] + list(STOPWORDS)
positive_wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white", stopwords = stop_words).generate(str(positive_tweets))
plt.figure()
plt.title("Tweets Positivos+ - Wordcloud")
plt.imshow(positive_wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# Wordcloud with positive tweets
pos_tweets = df['Tweet'][df["Predicción"] == 'P']
stop_words = ["https", "co", "RT", "la", "en", "que", "de", "una", "un", "los", "y", "lo", "mi", "te" ] + list(STOPWORDS)
positive_wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white", stopwords = stop_words).generate(str(positive_tweets))
plt.figure()
plt.title("Tweets Positivos - Wordcloud")
plt.imshow(positive_wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
# Wordcloud with positive tweets
negative_tweets = df['Tweet'][df["Predicción"] == 'N']
stop_words = ["https", "co", "RT", "la", "en", "que", "de", "una", "un", "los", "y", "lo", "mi", "te" ] + list(STOPWORDS)
positive_wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white", stopwords = stop_words).generate(str(positive_tweets))
plt.figure()
plt.title("Tweets Negativos - Wordcloud")
plt.imshow(positive_wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
# Wordcloud with positive tweets
neg_tweets = df['Tweet'][df["Predicción"] == 'N+']
stop_words = ["https", "co", "RT", "la", "en", "que", "de", "una", "un", "los", "y", "lo", "mi", "te" ] + list(STOPWORDS)
positive_wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white", stopwords = stop_words).generate(str(positive_tweets))
plt.figure()
plt.title("Tweets Negativos+ - Wordcloud")
plt.imshow(positive_wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()