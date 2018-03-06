#import the library used to query a website
import urllib3

#import the Beautiful soup functions to parse the data returned from the website
from bs4 import BeautifulSoup

import pandas as pd
from ast import literal_eval as le
import gensim

import wikipedia
import logging

import PyPDF2
import glob

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

import os

dataset_dir_name = "\\Dataset\\"
datadump_dir_name = "\\Data_Dump\\"
datadump_filename = "data_dump.csv"
df_columns = ['presentation data','context']

#Extraction of data-----------------------------
def create_datadump(dataset_dir,datadump_dir):
    files = get_files(dataset_dir)
    data_dump = []
    for file in files:
        pdf_text, context = pdf_to_text(file)
        pdf_text = preprocessing(pdf_text)
        data_dump += [[pdf_text, context]]
    datadump_df = pd.DataFrame(data_dump, index=files, columns=df_columns)
    datadump_df.to_csv(os.getcwd()+datadump_dir_name+datadump_filename,compression="gzip")
    
def check_datadump_exists():
    datadump_dir = os.getcwd()+datadump_dir_name
    return os.path.exists(datadump_dir+datadump_filename)

def get_search_term(filename):
    filename = filename.replace("_"," ")
    filename = filename[:(len(filename)-4)]
    context = ""
    words = nltk.word_tokenize(filename)
    words = preprocessing(words)
    tags = nltk.pos_tag(words)
    for tag in tags:
        if tag[1] == 'NNP':
            context = context + web_api(tag[0]) +" "
    return context
    
def web_scrapper(search):    
    http = urllib3.PoolManager()
    urllib3.disable_warnings()
    
    #specify the url
    wiki = "http://en.wikipedia.org/wiki/" + search

    #Query the website and return the html to the variable page
    page = http.request('GET',wiki)
    
    #Parse the html in the age variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(page.data,"lxml")
    paras = soup.find_all("p")
    return str(paras[0].get_text())
    
def web_api(search):
    page_summary = ""
    try:
        page = wikipedia.page(search)
        if page is None:
            page_summary = page.summary
    except Exception as e:
        logging.exception("Custom Exceptions:\nsearch:"+search+"\nError:"+str(e))
    return page_summary

def pdf_to_text(filename):
    context = ''
    pdf_text = ''
    file_obj = open(filename,'rb')
    #context = get_search_term(filename)
    pdfReader = PyPDF2.PdfFileReader(file_obj)
    for i in range(0,pdfReader.numPages):
        page_obj = pdfReader.getPage(i)
        pdf_text = pdf_text + page_obj.extractText()
    file_obj.close()
    return pdf_text, context

def get_files(dataset_dir):
    files = glob.glob(dataset_dir+"*.pdf")
    return files

#Extraction of data ends---------------------------

#Preprocessing-------------------------

def preprocessing(data):
    if type(data) is str:
        data = clean_data(data)
        words = word_tokenize(data)
    elif type(data) is list:
        words = data
    else:
        print("Error")
    words = remove_punctuations(words)
    words = convert2lower(words)
    filtered_words = remove_stopwords(words)
    unique_word_list = remove_duplicates(filtered_words)                
    return unique_word_list

def convert2lower(words):
    words = [word.lower() for word in words]
    return words

def clean_data(data):
    data = rem_extra_chars(data)
    return data

def rem_extra_chars(data):
    data = data.replace("\n", " ")
    return data

def remove_punctuations(words):
    words = [word for word in words if word.isalpha()]
    return words    

def remove_stopwords(words):
    stop_words = set(stopwords.words('english'))
    filtered_words = [w for w in words if not w in stop_words]
    return filtered_words

def stemming(filtered_words):
    stemmer = PorterStemmer()
    stemmed_words = []
    for word in filtered_words:
        if word != "" or word != '':
            stemmed_words += stemmer.stem(word)
    return stemmed_words

def lemmatizing(filtered_words):
    lemmatized_words = []
    lmtzr = WordNetLemmatizer()
    for word in filtered_words:
        lemmatized_words += lmtzr.lemmatize(word)
    
def remove_duplicates(stemmed_words):
    stemmed_set = set(stemmed_words)
    seen_set = set()
    unique_word_list = []
    for word in stemmed_set:
        if word not in seen_set:
            seen_set.add(word)
            unique_word_list.append(word)
    return unique_word_list

def ner_tagger(word_list):
    ner_tagged = nltk.pos_tag(word_list)
    return ner_tagged

#Preprocessing ends-------------------------


#Data dictionary --------------------------------
def create_datadict():
    datadump_df = pd.read_csv(os.getcwd()+datadump_dir_name+datadump_filename,compression='gzip')
    word_list = []
    for index,row in datadump_df.iterrows():
        word_list += le(row[df_columns[0]])
    
    
    
#Data dictionary ends----------------------------

dataset_dir = os.getcwd()+dataset_dir_name
datadump_dir = os.getcwd()+datadump_dir_name
if check_datadump_exists()==False:
    create_datadump(dataset_dir, datadump_dir)
create_datadict()