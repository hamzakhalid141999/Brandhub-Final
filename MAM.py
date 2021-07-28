from flask import Flask
from flask_restful import Api,Resource
import numpy as np
import cv2
import imutils
import argparse
import glob
import matplotlib.pyplot as plt
import pymongo
from pymongo import MongoClient
from PIL import Image
import json
import requests
from os.path  import basename
import os
import os.path
from os import path
import requests
# from ipynb.fs.full.SBIIteration3 import * 
from tensorflow import keras
import FullNonFull

from ast import literal_eval
import Topbottom1
import EasternWestern1
from flask_cors import CORS


app=Flask(__name__)
api=Api(app)
CORS(app)

# FinalResults={}
Final_Dict={} #will contain shirts and bottoms (result of both SBI IA)
class MakeAMatch(Resource):
	def get(self,imagePath,gender):
		# FinalResults={}
		cd = ColorDescriptor((8, 12, 3))

		FinalResults={}
		FinalResults,TypeEW=MatchProducts(imagePath,gender)
		Final={}
		finalResult={}
		product_count=1
		Final = sorted([ (k,v) for k,v in FinalResults.items()]) #sort result dictionary
		# Final=Final[:10] #returns 10 top ptoducts
		print(Final)

		client = pymongo.MongoClient("mongodb+srv://zahra:passmongodb@cluster0.femwg.mongodb.net/test?retryWrites=true&w=majority")

		if (gender=='F'):
			db=client['Female']
		else:
			db=client['Male']
		db_collection=db[TypeEW]
		for (resID,arr) in Final:
			print("1ST SBI: "+resID)
			dict1=db_collection.find_one({'PId': resID}) #get data from male db
			prod={}
			if (dict1!=None):
				for key,val in dict1.items():
					if (key!='featureVectors' and key!='_id'): #cuz featureVectors are very long and output gets confusing
						prod[key]=val
						print(str(key)+ " : "+str(val))
			finalResult[product_count]=prod
			product_count+=1
			print("Resultssss:")
			for (score,prod_res_ID) in arr.items():

				dict1=db_collection.find_one({'PId': prod_res_ID}) #get data from male db

				prod={}
				if (dict1!=None):
					for key,val in dict1.items():
						if (key!='featureVectors' and key!='_id'): #cuz featureVectors are very long and output gets confusing
							prod[key]=val
							print(str(key)+ " : "+str(val))
				finalResult[product_count]=prod
				product_count+=1
		
		
		# for (score,resID) in Final:
		# #     print(score+ resID)
		# 	if (gender=='F'):
		# 		db=client['Female']
		# 	else:
		# 		db=client['Male']
		# 	db_collection=db[TypeEW]
			
		# 	dict1=db_collection.find_one({'PId': resID}) #get data from male db
			
			
		# 	if (dict1!=None):
		# 		prod={}
		# 		for key,val in dict1.items():
		# 			if (key!='featureVectors' and key!='_id'): #cuz featureVectors are very long and output gets confusing
		# 				prod[key]=val
		# 				print(str(key)+ " : "+str(val))

		# 	finalResult[product_count]=prod
		# 	product_count+=1
		return finalResult




def getWidthHeight(height,width,Type,FullHalf):
	if (FullHalf=='Full'):
		TopWidthStart=int(width // 2.4)
		TopWidthStop=int(width //1.7)
		TopHeightStart=int (height // 5)
		BotHeightStop=  int(height // 1.17)
		if (Type=='Eastern'):
			TopHeightStop=int (height // 1.5)
			BotHeightStart=int(height // 1.4)

		elif (Type=='Western'):
			TopHeightStop= int (height // 2.5)
			BotHeightStart=int(height // 2)
	else:
		TopWidthStart=int(width // 2.5)
		TopWidthStop=int(width //2)
		TopHeightStart=int (height // 4)
		BotHeightStop=  height
		if (Type=='Eastern'):
			TopHeightStop=int (height // 1.4)
			BotHeightStart=int(height // 1.5)

		elif (Type=='Western'):
			TopHeightStop= int (height // 1.5)
			BotHeightStart=int(height // 1.4)
			
	return TopHeightStart,TopHeightStop,TopWidthStart,TopWidthStop,BotHeightStart,BotHeightStop

class ColorDescriptor:
	def __init__(self, bins):
	# store the number of bins for the 3D histogram
		self.bins = bins

	def histogram(self, image, mask):
	# extract a 3D color histogram from the masked region of the
	# image, using the supplied number of bins per channel
		hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,[0, 180, 0, 256, 0, 256])
		# normalize the histogram if we are using OpenCV 2.4
		if imutils.is_cv2():
			hist = cv2.normalize(hist).flatten()
		# otherwise handle for OpenCV 3+
		else:
			hist = cv2.normalize(hist, hist).flatten()
		# return the histogram
		return hist

	def describe(self, image):
		# convert the image to the HSV color space and initialize
		# the features used to quantify the image
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		features = []
		# grab the dimensions and compute the center of the image
		(h, w) = image.shape[:2]
		(cX, cY) = (int(w * 0.5), int(h * 0.5))
		# construct an elliptical mask representing the center of the
		# image
		(axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
		
		angle=0
		ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
		ellipMask=cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), angle, 0, 360, 255, -1) 
		# extract a color histogram from the elliptical region and
		# update the feature vector
		hist = self.histogram(image, ellipMask)
		features.extend(hist)
		# return the feature vector
		return features

cd = ColorDescriptor((8, 12, 3))


class Searcher:

	def search( queryFeatures,gender,typeEW,category,thresh,limit):
		results = {}
		client = pymongo.MongoClient("mongodb+srv://zahra:passmongodb@cluster0.femwg.mongodb.net/test?retryWrites=true&w=majority")
	   
		
		if (gender=='F'): 
			Gender='Female'
		else:
			Gender='Male'
		
		queryID = {'PId': {'$exists': 1},}
		projectionID = {'_id': 0, 'PId': 1}
	 
		queryT = {'Category': {'$exists': 1},}
		projectionT = {'_id': 0, 'Category': 1}
		
		#query to get feature vectors
		queryFV = {'featureVectors': {'$exists': 1},}
		projectionFV = {'_id': 0, 'featureVectors': 1}
		
		
		brand_count=0
		print("Gender is: "+ Gender)
		db = client[Gender]
		print("Calculating distances..")
		
		db_collection=db[typeEW]
 
		typels=list(db_collection.find(queryT, projectionT))
		arrId=list(db_collection.find(queryID, projectionID))
		titles=[]
		types=[]

#         res = OrderedDict(reversed(arrId)
		arrId.reverse();
		typels.reverse();
		
		for type1 in typels:
			for key,value in type1.items():
				types.append(value) #store type of product in types array to retrieve type of products
		print(len(typels))

		products = list(db_collection.find(queryFV, projectionFV)) #access women portion of brand from db
		products.reverse();
		print(len(products))
		product_count=0
		for product in products: #iterate thru all products in db
		   
			image_count=1
			id_val=""
			check_wrong=0
			for key, value in product.items():
				fVector=literal_eval(value) #convert string from db into list

				resultValue=2.5 #max distance value
				d=2
				check=0
				check_wrong=0
				check_okay=0
				
				if (category=="bottom" and types[product_count]=="Bottom"):
					check_okay=1
				elif (category=="top" and types[product_count]=="Top"):
					check_okay=1
				else:
					check_okay=0
#                 print(str(arrId[product_count])+ str(fVector))    
				if (check_okay==1):
					for f in fVector:
#                         if (check!=1): #check=1 means distance of FV of product is greater than 1.5 so skip remaining FV of same product
						   
						d = Searcher.chi2_distance(f, queryFeatures) #pass indices from feature vectors to calculate distance
#                         print(str(arrId[product_count])+" "+str(d))
#                         if (d>thresh): #if distance is greater than max value then don't loop further thru images
#                             check=1
#                             break;
						if d<resultValue:
							resultValue=d
					if (resultValue<thresh): #if distance is less than 1.5 then store in results
						s=0
						dict2=db_collection.find_one({'featureVectors':str(fVector)})
						for (resID,arr) in Final_Dict.items():
							if (dict2['PId'] in arr.values()):
								s=1 #do nothing
						if (s!=1):
							results[dict2['PId']] = resultValue #store the distance of products with its title in dictionary
						
#                     else:
#                         break; #if distance is greater than 1.5, don't loop further

			product_count+=1
		brand_count+=1

		results = sorted([(v, k) for (k, v) in results.items()]) #sort result dictionary
		print("Done!"+str(len(results)))
		return results[:limit] #returns 10 top ptoducts

   

	def chi2_distance(histA, histB, eps = 1e-10):
		# compute the chi-squared distance
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])
		# return the chi-squared distance
		return d

def opposite(topbottom):
	imagetype=""
	if (topbottom=='top'):
		topbottom='bottom'
		imagetype='f2.jpg'
	else:
		topbottom='top'
		imagetype='f1.jpg'
	return topbottom,imagetype

def getThreshold(gender):
	if (gender=='F'):
		threshold=1.5
	else:
		threshold=1.5
	return threshold

def MatchItems(image,itemType,gender,TypeEW):
	FinalResults={}
	
	thresh=getThreshold(gender)
	
	query = cv2.imread(image)
	features = cd.describe(query)
	
	
	results=Searcher.search(features,gender,TypeEW,itemType,thresh,3)
	for (key,val) in results:
		if (FinalResults!=None):
			if (val in FinalResults.values()): #so same products don't appear in results
				s=0
			else:
				FinalResults[key]=val
		else:
			FinalResults[key]=val
#     print("FINAL")
#     print(FinalResults)
	return len(FinalResults),FinalResults

def MatchProducts(queryImage,gender):
	thresh=getThreshold(gender)
	
	FinalResults={}
	query = cv2.imread(queryImage)
	features = cd.describe(query)
	mod=keras.models.load_model("TopBottom_model")
	Type_TB=""
	Type_TB=Topbottom1.computeCategory(queryImage,mod)
	mod2=keras.models.load_model("EasternWestern_model")
	TypeEW=""
	TypeEW= EasternWestern1.computeCategory(queryImage,mod2)
	results=Searcher.search(features,gender,TypeEW,Type_TB,2,5)
	print(results)
	check=0
	FinalResults_len=0
	
	for (score, resultID) in results:
		
		# if (FinalResults_len<10):
		image_count=1
		NFull_image_count=1
		print(TypeEW)
		imagePath="C:/Users/hp/practice/BrandHub/BrandHub-main/"+TypeEW+"/"+resultID
		image_path="C:/Users/hp/practice/BrandHub/BrandHub-main/"+TypeEW+"/"+str(resultID)+str(image_count)+".jpg"
		if (path.exists(image_path)): #check if path exists
			mod=keras.models.load_model("Full_model")
			Type_FN=""
			Type_FN= FullNonFull.computeCategory(image_path,mod)
			img = cv2.imread(image_path)
			height = img.shape[0]
			width = img.shape[1]

			if (Type_FN=='Full'):
				h1,h2,w1,w2,h3,h4=getWidthHeight(height,width,TypeEW,'Full') #get dimensions for extracting color

			else:
				h1,h2,w1,w2,h3,h4=getWidthHeight(height,width,TypeEW,'NFull')


			s1 = img[h1:h2, w1:w2] #split img in 2 parts based on dimension
			s2 = img[h3:h4, w1:w2]

			cv2.imwrite("f1.jpg", s1) #save images in files
			cv2.imwrite("f2.jpg", s2)

			matchItem,image_No=opposite(Type_TB) #get top if bottom and bottom if top

			temp_result={}
			FinalResults_len,temp_result=MatchItems(image_No,matchItem,gender,TypeEW)
			Final_Dict[resultID]=temp_result
			image_count=0
		# else:
		# 	print("FINISHED!")
	return Final_Dict,TypeEW
		
		
	
	

api.add_resource(MakeAMatch,"/mam/<string:imagePath>/<string:gender>")

if __name__=="__main__":
	app.run(debug=True, port=5004)