import pymongo
from pymongo import MongoClient

import json
import requests

import pandas as pd

import langdetect


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

from gensim.models import Doc2Vec
from collections import namedtuple
import gensim.utils
from langdetect import detect
import re
import string

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from nltk.corpus import stopwords
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import nltk
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk.stem import PorterStemmer
from colour import Color

def check_color(color): #extracts color from description for khaadi
    try:
        Color(color)
        return True
    except ValueError:
        return False

#clean the data-> apply stemming, remove stopwords then punctuation and then use specific POS
def CleanData(string):
    stop_words = set(stopwords.words('english')) #set language of stopwords
    ps = PorterStemmer() #initialize stemming
    word_tokens = word_tokenize(string)
    filtered_sentence = []
    
    #removing stopwords:
    for w in word_tokens:
        if w not in stop_words:
            w=ps.stem(w) #applying stemming
            filtered_sentence.append(w)
    
    listToStr = ' '.join(map(str, filtered_sentence)) #convert list to str
    
    #remove unwanted characters
    newStr=listToStr.replace('.','')
    newStr=newStr.replace('%','')
    newStr=newStr.replace('\n',' ')
    text = word_tokenize(newStr) #tokenize string
    
    #POS tagging. Only keep words that are nouns,adjectives,verbs
    x=nltk.pos_tag(text)
    i=0
    finalStr=""
    for k in range(0,len(x)):
        if x[i][1]=="NNS" or  x[i][1]=="NN" or  x[i][1]=="NNP" or x[i][1]=="JJ" or x[i][1]=="JJR" or x[i][1]=="JJS" or x[i][1]=="NN" or x[i][1]=="VB" or x[i][1]=="VBD" or x[i][1]=="VBN" or x[i][1]=="VBP":
            finalStr+=x[i][0]
            finalStr+=" "
        i+=1
    return finalStr #return cleaned string



#get data from db
client = pymongo.MongoClient("mongodb+srv://zahra:passmongodb@cluster0.femwg.mongodb.net/test?retryWrites=true&w=majority")

#query for Outfitters
queryO = {'PId': {'$exists': 1},'PName': {'$exists': 1},'Color': {'$exists': 1},'Fabric': {'$exists': 1},'Type': {'$exists': 1},'Description': {'$exists': 1}}
projectionO = {'_id': 0,'PId':1,'_id': 0,'PName':1,'_id': 0,'Color':1,'_id': 0,'Fabric':1,'_id': 0,'Type':1,'_id': 0,'Description':1}

#query for Sapphire
queryS = {'PId': {'$exists': 1},'Color': {'$exists': 1},'Fabric': {'$exists': 1},'Type': {'$exists': 1},'Description': {'$exists': 1}}
projectionS = {'_id': 0,'PId':1,'_id': 0,'Color':1,'_id': 0,'Fabric':1,'_id': 0,'Type':1,'_id': 0,'Description':1}

#query for Khaadi
queryk = {'PId': {'$exists': 1},'Fabric': {'$exists': 1},'PName': {'$exists': 1},'Description': {'$exists': 1}}
projectionk = {'_id': 0,'PId':1,'_id': 0,'Fabric':1,'_id': 0,'PName':1,'_id': 0,'Description':1}

#query for Jdot
queryJ = {'PId': {'$exists': 1},'Color': {'$exists': 1},'Fabric': {'$exists': 1},'Type': {'$exists': 1},'Details': {'$exists': 1}}
projectionJ = {'_id': 0,'PId':1,'_id': 0,'Color':1,'_id': 0,'Fabric':1,'_id': 0,'Type':1,'_id': 0,'Details':1}

#query for Limelight
queryL = {'PId': {'$exists': 1},'Fabric': {'$exists': 1},'PName': {'$exists': 1},'Description': {'$exists': 1}}
projectionL = {'_id': 0,'PId':1,'_id': 0,'Fabric':1,'_id': 0,'PName':1,'_id': 0,'Description':1}

#query for Cambridge
queryC = {'PId': {'$exists': 1},'Color': {'$exists': 1},'Fabric': {'$exists': 1},'Type': {'$exists': 1},'Description': {'$exists': 1}}
projectionC = {'_id': 0,'PId':1,'_id': 0,'Color':1,'_id': 0,'Fabric':1,'_id': 0,'Type':1,'_id': 0,'Description':1}

query1 = {'PId': {'$exists': 1},}
projection1 = {'_id': 0, 'PId': 1}



s=0

gender_check=False

MenBrands=['Cambridge','Outfitters','Jdot'] #men brands
WomenBrands=['Limelight','khaadi','sapphire','Outfitters','Jdot'] #women brands
AllBrands=['Limelight','khaadi','sapphire','Outfitters','Jdot','Cambridge'] #all brands
gender=['Men','Women']
i=0
j=0


for g in gender: #iterate for both genders
    brands=AllBrands #store data of all brands in arrays
    s=0
    for b in brands:
        brand=brands[s] #running for this brand
        print(brand)
        db = client[brand] #specify brand to db
        
        if (brand==brands[0]): #brand is Limelight so store corresponding query and projection
            query=queryL
            projection=projectionL
            
        if (brand==brands[1]): #if brand is khaadi. separate if condition so we can extract color from description
            products = list(db[g].find(queryk, projectionk)) #convert query to list
            for product in products: #iterate list of all products
                string=""
                PID=""
                for key, value in product.items(): #iterate through all items in each product
                    if (key!='PId' and key!='Description'): #store data if not the id and description
                        string+=value
                        string+=" "
                    if (key=='Description'):
                        _color=[i for i in value.split('_') if check_color(i)] #extract color from description
                        string+=_color[0]
                    if (key=='PId'):
                        PID=value #store product id to update db later on 

                cleanedstring=CleanData(string) #clean data of product

                #update product with textsearch that contains processed data
                db_collection=db[g]
                db_collection.update_one(  { 'PId':PID} , { '$set': { 'textSearch' : cleanedstring  } } ) 
        
        elif (brand==brands[2]): #brand is Sapphire so store corresponding query and projection
            if (g==gender[0]):
                gender_check=True #sapphire doesn't have men so if gender is men don't store query. check is set to true so db isn't updated
            else:
                query=queryS
                projection=projectionS

        elif (brand==brands[3]): #brand is Outfitters so store corresponding query and projection
            query=queryO
            projection=projectionO
            
        elif (brand==brands[4]): #brand is Jdot so store corresponding query and projection
            query=queryJ
            projection=projectionJ
            
        elif (brand==brands[5]): #brand is Cambridge so store corresponding query and projection
            if (g==gender[1]):
                gender_check=True #Cambridge doesn't have women so if gender is women don't store query. check is set to true so db isn't updated
            else:
                query=queryC
                projection=projectionC
        

        
        print("Brand: "+brand)
        print("Gender: "+g)
        if (brand!=brands[1] and gender_check!=True): #if brand isn't khaadi and brand has specified gender
            db=client[brand] #tell brand to db
            db_collection=db[g] #tell gender to db
            products = list(db_collection.find(query, projection)) #run query and store in list

            for product in products: #iterate through all items in each product
                string=""
                for key, value in product.items(): #iterate through all items in each product
                    if (key!='PId'):
                        string+=value #store all data except for id
                        string+=" "
                    if (key=='PId'):
                        PID=value #store product id to update db later on 
                cleanedstring=CleanData(string) #clean data of product

                #update product with textsearch that contains processed/cleaned data
                db_collection.update_one(  { 'PId':PID} , { '$set': { 'textSearch' : cleanedstring } } )
        gender_check=False
        s+=1




