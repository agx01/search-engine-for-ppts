# -*- coding: utf-8 -*-

def pdf_to_text(filename):
    import PyPDF2
    file_obj = open(filename,'rb')
    get_search_term(filename)
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
    import os
    fullfilename = os.path.join(os.getcwd(),filename)
    ppt = comtypes.client.CreateObject("Powerpoint.Application")
    ppt.Visible = 1
    deck = ppt.Presentations.Open(fullfilename)
    newname = os.path.splitext(filename)[0]+".pdf"
    fullnewname = os.path.join(os.getcwd(),"pdf",newname)
    deck.SaveAs(fullnewname,formatType)
    deck.Close()
    ppt.Quit()

def get_search_term(filename):
    filename = filename.replace("_"," ")
    filename = filename[:(len(filename)-4)]
    print(filename)
    import nltk
    words = nltk.word_tokenize(filename)
    tags = nltk.pos_tag(words)
    print(tags)

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

import platform
import glob

files = glob.glob("*.ppt")+glob.glob("*.pptx")

if(platform.system()=='Windows'):
    pdf_to_text("HSBC_Research_PaperContent.pdf")
else:
    print('0')
    


