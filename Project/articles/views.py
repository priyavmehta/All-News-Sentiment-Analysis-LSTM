from flask import Blueprint, render_template, url_for, request, redirect, flash
from Project import db
import requests
from newspaper import Article
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from Project.models import Articles
from datetime import datetime
import time
from tensorflow.keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle
import re

article = Blueprint('article',__name__)

max_length = 1000

def preprocessor(text):
    text = re.sub('<[^>]*>','',text)
    
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',text)
    text = re.sub('[\W]+',' ', text.lower()) +\
        ' '.join(emoticons).replace('-', '')
    
    return text

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = [lemmatizer.lemmatize(token) for token in text.split(" ")]
    text = [lemmatizer.lemmatize(token, "v") for token in text]
    text = [word for word in text if not word in stop_words]
    text = " ".join(text)
    return text

@article.route('/')
def index():
    return  render_template('home.html')

@article.route('/businessNews')
def business_news():
    model = load_model('sentiment_analysis_lstm_model.h5')
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    print(model)
    url = 'http://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=d28171203ba44061800380cdf2e7ebbf'
    data = requests.get(url).json()
    print(len(data))
    my_articles = data['articles']

    articles=[]

    for article in my_articles:
        description = article['description']
        author = article['author']
        title = article['title']
        source = article['source']['name']
        url = article['url']
        url_to_image = article['urlToImage']
        published_date = article['publishedAt']
        string = published_date.split('T')
        string = string[0] + ' ' +string[1][:-1]
        print(string)
        date = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        article_type = 'business'
        myArticle = Article(url, language="en")
        myArticle.download()
        myArticle.parse()
        myArticle.nlp()
        summary = myArticle.summary

        text = preprocessor(summary)
        text = clean_text(text)
        text = tokenizer.texts_to_sequences([text])
        text = pad_sequences(text,maxlen=max_length)
        probability = model.predict(text)[0][0]
        print(probability)
        sentiment = ''

        if probability > 0.5:
            sentiment = 'Positive'
        
        else:
            sentiment = 'Negative'

        dummy = Articles(description=description,author=author,title=title,source=source,url=url,url_to_image=url_to_image,published_date=date,article_type=article_type,summary=summary,sentiment=sentiment,probability=str(probability))
        articles.append(dummy)
    #print(myArticle.summary)
    return render_template('business.html',articles=articles)


@article.route('/sportsNews')
def sports_news():
    model = load_model('sentiment_analysis_lstm_model.h5')
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    url = 'http://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=d28171203ba44061800380cdf2e7ebbf'
    data = requests.get(url).json()
    print(len(data))
    my_articles = data['articles']

    articles=[]

    for article in my_articles:
        description = article['description']
        author = article['author']
        title = article['title']
        source = article['source']['name']
        url = article['url']
        url_to_image = article['urlToImage']
        published_date = article['publishedAt']
        string = published_date.split('T')
        string = string[0] + ' ' +string[1][:-1]
        print(url_to_image)
        date = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        article_type = 'business'
        myArticle = Article(url, language="en")
        myArticle.download()
        myArticle.parse()
        myArticle.nlp()
        summary = myArticle.summary

        text = preprocessor(summary)
        text = clean_text(text)
        text = tokenizer.texts_to_sequences([text])
        text = pad_sequences(text,maxlen=max_length)
        probability = model.predict(text)[0][0]
        print(probability)
        sentiment = ''

        if probability > 0.5:
            sentiment = 'Positive'
        
        else:
            sentiment = 'Negative'

        dummy = Articles(description=description,author=author,title=title,source=source,url=url,url_to_image=url_to_image,published_date=date,article_type=article_type,summary=summary,sentiment=sentiment,probability=str(probability))
        articles.append(dummy)
    #print(myArticle.summary)
    return render_template('sports.html',articles=articles)

@article.route('/healthNews')
def health_news():
    
    model = load_model('sentiment_analysis_lstm_model.h5')
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    url = 'http://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=d28171203ba44061800380cdf2e7ebbf'
    data = requests.get(url).json()
    print(len(data))
    my_articles = data['articles']

    articles=[]

    for article in my_articles:
        description = article['description']
        author = article['author']
        title = article['title']
        source = article['source']['name']
        url = article['url']
        url_to_image = article['urlToImage']
        published_date = article['publishedAt']
        string = published_date.split('T')
        string = string[0] + ' ' +string[1][:-1]
        print(url_to_image)
        date = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        article_type = 'business'
        myArticle = Article(url, language="en")
        myArticle.download()
        myArticle.parse()
        myArticle.nlp()
        summary = myArticle.summary

        text = preprocessor(summary)
        text = clean_text(text)
        text = tokenizer.texts_to_sequences([text])
        text = pad_sequences(text,maxlen=max_length)
        probability = model.predict(text)[0][0]
        print(probability)
        sentiment = ''

        if probability > 0.5:
            sentiment = 'Positive'
        
        else:
            sentiment = 'Negative'

        dummy = Articles(description=description,author=author,title=title,source=source,url=url,url_to_image=url_to_image,published_date=date,article_type=article_type,summary=summary,sentiment=sentiment,probability=str(probability))
        articles.append(dummy)
    #print(myArticle.summary)
    return render_template('health.html',articles=articles)

@article.route('/scienceNews')
def science_news():
    model = load_model('sentiment_analysis_lstm_model.h5')
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    url = 'http://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=d28171203ba44061800380cdf2e7ebbf'
    data = requests.get(url).json()
    print(len(data))
    my_articles = data['articles']

    articles=[]

    for article in my_articles:
        description = article['description']
        author = article['author']
        title = article['title']
        source = article['source']['name']
        url = article['url']
        url_to_image = article['urlToImage']
        published_date = article['publishedAt']
        string = published_date.split('T')
        string = string[0] + ' ' +string[1][:-1]
        print(url_to_image)
        date = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        article_type = 'business'
        myArticle = Article(url, language="en")
        summary=''
        sentiment = ''
        try:
            myArticle.download()
            myArticle.parse()
            myArticle.nlp()
            summary = myArticle.summary

            text = preprocessor(summary)
            text = clean_text(text)
            text = tokenizer.texts_to_sequences([text])
            text = pad_sequences(text,maxlen=max_length)
            probability = model.predict(text)[0][0]
            print(probability)

            if probability > 0.5:
                sentiment = 'Positive'
            
            else:
                sentiment = 'Negative'
        except:
            pass

        dummy = Articles(description=description,author=author,title=title,source=source,url=url,url_to_image=url_to_image,published_date=date,article_type=article_type,summary=summary,sentiment=sentiment,probability=str(probability))
        articles.append(dummy)
    #print(myArticle.summary)
    return render_template('science.html',articles=articles)

@article.route('/technologyNews')
def technology_news():
    model = load_model('sentiment_analysis_lstm_model.h5')
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    url = 'http://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=d28171203ba44061800380cdf2e7ebbf'
    data = requests.get(url).json()
    print(len(data))
    my_articles = data['articles']

    articles=[]

    for article in my_articles:
        description = article['description']
        author = article['author']
        title = article['title']
        source = article['source']['name']
        url = article['url']
        url_to_image = article['urlToImage']
        published_date = article['publishedAt']
        string = published_date.split('T')
        string = string[0] + ' ' +string[1][:-1]
        print(url_to_image)
        date = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        article_type = 'business'
        myArticle = Article(url, language="en")
        summary=''
        sentiment = ''
        try:
            myArticle.download()
            myArticle.parse()
            myArticle.nlp()
            summary = myArticle.summary
            text = preprocessor(summary)
            text = clean_text(text)
            text = tokenizer.texts_to_sequences([text])
            text = pad_sequences(text,maxlen=max_length)
            probability = model.predict(text)[0][0]
            print(probability)

            if probability > 0.5:
                sentiment = 'Positive'
            
            else:
                sentiment = 'Negative'
        except:
            pass
        
        dummy = Articles(description=description,author=author,title=title,source=source,url=url,url_to_image=url_to_image,published_date=date,article_type=article_type,summary=summary,sentiment=sentiment,probability=str(probability))
        articles.append(dummy)
    #print(myArticle.summary)
    return render_template('technology.html',articles=articles)


@article.route('/generalNews')
def general_news():
    model = load_model('sentiment_analysis_lstm_model.h5')
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    url = 'http://newsapi.org/v2/top-headlines?country=in&pageSize=17&apiKey=d28171203ba44061800380cdf2e7ebbf'
    data = requests.get(url).json()
    print(len(data))
    my_articles = data['articles']

    articles=[]

    for article in my_articles:
        description = article['description']
        author = article['author']
        title = article['title']
        source = article['source']['name']
        url = article['url']
        url_to_image = article['urlToImage']
        published_date = article['publishedAt']
        string = published_date.split('T')
        string = string[0] + ' ' +string[1][:-1]
        print(url_to_image)
        date = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        article_type = 'business'
        myArticle = Article(url, language="en")
        myArticle.download()
        myArticle.parse()
        myArticle.nlp()
        summary = myArticle.summary

        text = preprocessor(summary)
        text = clean_text(text)
        text = tokenizer.texts_to_sequences([text])
        text = pad_sequences(text,maxlen=max_length)
        probability = model.predict(text)[0][0]
        print(probability)
        sentiment = ''

        if probability > 0.5:
            sentiment = 'Positive'
        
        else:
            sentiment = 'Negative'

        dummy = Articles(description=description,author=author,title=title,source=source,url=url,url_to_image=url_to_image,published_date=date,article_type=article_type,summary=summary,sentiment=sentiment,probability=str(probability))
        articles.append(dummy)
    #print(myArticle.summary)
    return render_template('general.html',articles=articles)