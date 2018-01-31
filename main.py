# -*- coding: utf-8 -*-
import pandas as pd
import os
import nltk
import platform

def get_search_terms(filename):
    filename = filename.replace("_"," ")
    filename = filename[:(len(filename)-4)]
    searches = []
    words = nltk.word_tokenize(filename)
    tags = nltk.pos_tag(words)
    for tag in tags:
        if tag[1] == 'NNP':
            searches.append(tag)
    return searches

def get_context(filename):
    searches = get_search_terms(filename)
    context = ""
    for search in searches:
        try:
            context += web_scrapper(search) + " "
        except:
            print("Using wikipedia API")
        finally:
            context += web_api(search) + " "
    return context

def web_api(search):
    import wikipedia
    page = wikipedia.page(search)
    return page.summary

def web_scrapper(search):    
    #import the library used to query a website
    import urllib3
    http = urllib3.PoolManager()
    urllib3.disable_warnings()
    
    #specify the url
    wiki = "http://en.wikipedia.org/wiki/" + search

    #Query the website and return the html to the variable page
    page = http.request('GET',wiki)
    
    #import the Beautiful soup functions to parse the data returned from the website
    from bs4 import BeautifulSoup
    
    #Parse the html in the age variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(page.data,"lxml")
    paras = soup.find_all("p")
    return str(paras[0].get_text())

def pdf_to_text(filename):
    import PyPDF2
    file_obj = open(filename,'rb')
    context = get_context(filename)
    pdf_text = ''
    pdfReader = PyPDF2.PdfFileReader(file_obj)
    for i in range(0,pdfReader.numPages):
        page_obj = pdfReader.getPage(i)
        pdf_text = pdf_text + page_obj.extractText()
    file_obj.close()
    return pdf_text

#comtypes not working to save the ppt as a pdf
def ppt_to_pdf(filename,formatType=32):
    import comtypes.client
    fullfilename = os.path.join(os.getcwd(),filename)
    ppt = comtypes.client.CreateObject("Powerpoint.Application")
    ppt.Visible = 1
    deck = ppt.Presentations.Open(fullfilename)
    newname = os.path.splitext(filename)[0]+".pdf"
    fullnewname = os.path.join(os.getcwd(),"pdf",newname)
    deck.SaveAs(fullnewname,formatType)
    deck.Close()
    ppt.Quit()

def get_data_context(file):
   pass

def get_files(dataset_dir):
    import glob
    files = glob.glob(dataset_dir+"*.pdf")
    for file in files:
        

dataset_dir = "C:\\Work\\search-engine-for-ppts\\"
if(platform.system()=='Windows'):
    get_files(dataset_dir)
else:
    print('0')
    


