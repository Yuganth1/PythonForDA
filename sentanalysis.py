# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 19:09:40 2025

@author: yugan
"""

# Install wordcloud, langdetect, sumy, textblob
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from langdetect import detect
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer
from textblob import TextBlob
import seaborn as sns

#Reading csv file
df = pd.read_csv('C:/Users/yugan/OneDrive/Desktop/Py course/Data/Source (Input) Data for the course/Sentiment Analysis/chatgpt1.csv')

#Creating a function to detect language

x = df['Text'][0]
lang = detect(x)

def det(x):
    try:
        lang = detect(x)
    except: 
        lang = 'Other'
    return lang

df['Lang'] = df['Text'].apply(det)

df = df.loc[df['Lang'] == 'en']
df = df.reset_index(drop=True)

#Cleaning some text
df['Text'] = df['Text'].str.replace('https', '')
df['Text'] = df['Text'].str.replace('amp', '')
df['Text'] = df['Text'].str.replace('t.co', '')

#Developing sentiment function
def get_sentiment(text):
    sentiment = TextBlob(text).sentiment.polarity
    
    if sentiment > 0:
        return 'positive'
    elif sentiment < 0:
        return 'negative'
    else:
        return 'neutral'
    
df['sentiment'] = df['Text'].apply(get_sentiment)

#Generating wordcloud

comment_words = ''
stopwords = set(STOPWORDS)

for val in df.Text:
    val = str(val)
    tokens = val.split()
    comment_words = comment_words + " ".join(tokens) + " "

wordcloud = WordCloud(width=500, height=900, background_color = 'black', stopwords = stopwords,
                      min_font_size = 10).generate(comment_words)
plt.figure(figsize=(8,8))
plt.imshow(wordcloud)
plt.axis('off')
plt.tight_layout()
plt.show()

sns.set_style('whitegrid')
plt.figure(figsize=(10,6))

sns.countplot(x='sentiment',data =df)
plt.xlabel('Sentiment')
plt.ylabel('Count of sentiment')
plt.title('Sentiment distribution')
plt.show()





 





























