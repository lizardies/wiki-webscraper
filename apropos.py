#Here you can find the python code, I commented the code to make it as readible as possible. 

#!pip install BeautifulSoup
#!pip install selenium
#!pip install unidecode
#!pip install wikipedia

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import bs4
import re
import pandas as pd
import os
import re
import unidecode
import smtplib, email, ssl
from getpass import getpass
import time
from random import *
import time
from googletrans import Translator
import requests
import wikipedia

#finding sentence with word in wikipedia
def find_sentence_with_word(titel, word):
    #content on wikipedia with 'titel'
    text = wikipedia.page(titel).content
    #Split text in sentences
    lijst_text_voor = text.split('.')
    text = re.sub("[\(\[].*?[\)\]]", "", text)
    text = re.sub(r'(==[^==]*)?==', "", text)
    text = re.sub(r'(=[^=]*)?=', "", text)
    #skip titles of text
    lijst_text_na = text.split('.')
    x = 0
    #look for sentence that contains 'word' in list of sentences
    for i in lijst_text_na:
        if word in i:
            sentence = i  +'.'
            sentence = sentence.strip()
            x = 1
            break  
    if x == 0:
        for i in lijst_text_voor:
            if word in i:
                #print(i + '.')
                sentence = i +'.'
                sentence = sentence.strip()
                x = 1
                #print(x)
                break  
    if x == 0:
        sentence = ''
    return sentence
 
#----------BEGINNING WITH RANDOM PAGE 
#Open chrome driver
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome()
driver.implicitly_wait(30)
#Go to wikipedia
path = 'https://en.wikipedia.org/wiki/'
driver.get(path)
time.sleep(2)

#Find random wikipedia page
element = driver.find_element_by_id("n-randompage")
element.click()

#Get content
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')
#Find titel of page
tittle = soup.find("title").get_text(strip=True)[:-12]
#Get wikipedia content
wikipedia.set_lang("en")

#Open a HTML file named after the titel
cwd = os.getcwd()
textfile = open(cwd + "\\" + titel + ".html" , "w")
#Make list of words/sentences that can follow a new subject, be chosen from randomly
list_apropos_words = ['</b> I heard that:', '</b> I read that:','</b> the other day I learned that:', '</b> did you know that:', '</b> did I tell you that']
#Write beginning HTML page
already_used = []
close_sentence = ''
html_str = """
<html>
<head>
<title> Apropos Story Telling </title>\n
</head>
<body>"""
textfile.write(html_str)
textfile.write('Let me tell you something about <b>' + titel + '</b> :')

#pick a number of subjects to iterate through 
number_subjects = 7

#Start iterating process
for subject in range(0,number_subjects):
#find all linking words
    i=0
    websites = []
    text_words = []
    text = wikipedia.page(titel).content
    text = re.sub(r'(==[^==]*)?==', "", text)
    text = re.sub(r'(=[^=]*)?=', "", text)
    text = re.sub("[\(\[].*?[\)\]]", "", text)
    sentence = text.partition('.')[0] 
    #if the first sentence is too small, take the second one as well
    if len(sentence) < 30:
        sentence = text.split('.')[0]+text.split('.')[1]
        sentence = sentence.strip()
    try:
        textfile.write('<br>' + sentence )
        #if sentence start with 'did', end with question mark
        if 'did' in close_sentence:
            textfile.write('?')
        #otherwise, end with '.'
        else:
            textfile.write('.')
    except:
        pass
    try:
        soup = soup.find(id='bodyContent')
    except:
        break
    
    #make a list of all linking pages in the old wikipedia page
    try:
        for text in soup.find_all('p'):
            for link in text.find_all('a', href=True):
                if '/wiki/' in link['href']:
                    websites  += [link['href']]
                    text_words += [link.get_text(strip=True)]
                    i+=1
    except:
        break
        
    #get random new page from list of linking wikipedia pages
    try:
        randn = randint(0,i - 1)
        website = websites[randn]
        word = text_words[randn]
    except:
        break
    
    while True:
        #Take a new page if the page has already been gone through
        if word in already_used:
            randn = randint(0,i - 1)
            website = websites[randn]
            word = text_words[randn]
            continue
        #Get the new content of the page
        try:
            #driver = webdriver.Chrome()
            #driver.implicitly_wait(30)
            path = 'https://en.wikipedia.org' + website
            driver.get(path)
            page_sourci = driver.page_source
            soup = BeautifulSoup(page_sourci, 'lxml')
            break
        #If a new page doesn't exist, find another one
        except:
            randn = randint(0,i - 1)
            website = websites[randn]
            word = text_words[randn]
        
    #Do nothing if the new page is in the starting sentence of the wikipedia page
    if word in sentence:
        random =0
    #Otherwise, find the sentence in the old wikipedia page containing the chosen new page
    else:
        sentence = find_sentence_with_word(titel, word)
        try:
            textfile.write('<br>'+ sentence )
        except:
            textfile.write("<br> I don't even know anything about"+ titel + ", but I do know something about " + word + "which is:" )
    titel = soup.find("title").get_text(strip=True)[:-12]
    #introduce new subject with 'apropos'
    randi = randint(0,len(list_apropos_words) - 1)
    close_sentence = list_apropos_words[randi]
    already_used += [word]
    if subject <5 :
        textfile.write('<br> <br> Apropos <b>' + word +';'+ close_sentence )
    #in the last new subject, closing the text with last new subject
    if subject ==5 :
        textfile.write('<br> <br> Last thing to know, apropos <b>' + word + '</b> is that: \n\n')

textfile.write('<br><br> I hope you learned some things today, <br><br> Lots of love, <br> <br> P.A. Soprano.')        
textfile.write('</body> </html>')
textfile.close()
 
 
 
