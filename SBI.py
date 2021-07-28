from flask import Flask
from flask_restful import Api,Resource
import pymongo
from pymongo import MongoClient
import numpy as np
# !pip install opencv-python
# !pip install Pillow
# !pip install Google
# !pip install imutils
import cv2
import imutils
import argparse
import glob
# !pip install --upgrade google
import matplotlib.pyplot as plt
from flask_cors import CORS


from PIL import Image
import json
import requests

from os.path  import basename
import os
import os.path
from os import path
import requests
from ast import literal_eval
import Topbottom1
import EasternWestern1
from tensorflow import keras

app=Flask(__name__)
api=Api(app)
CORS(app)


class SearchByImage(Resource):
	def get(self,imagePath,gender):
		cd = ColorDescriptor((8, 12, 3))
		# load the query image and describe it
		

		from tensorflow import keras

		mod=keras.models.load_model("TopBottom_model")
		mod2=keras.models.load_model("EasternWestern_model")
		category=""
		category=Topbottom1.computeCategory(imagePath,mod)
		TypeEW=""
		TypeEW=EasternWestern1.computeCategory(imagePath,mod2)
		query = cv2.imread(imagePath)
		features = cd.describe(query) #create feature vectors of query
		results=Searcher.search(features,gender,TypeEW,category,10) #pass gender of search and feature vector of search image

		client = pymongo.MongoClient("mongodb+srv://zahra:passmongodb@cluster0.femwg.mongodb.net/test?retryWrites=true&w=majority")
		
		brandsName=['Limelight','khaadi','sapphire','Outfitters','Jdot','Cambridge'] #all brands
		product_count=1
		finalResult={}
		for (score, resultID) in results:
			if (gender=='F'):
				db=client['Female']
			else:
				db=client['Male']
				
			db_collection=db[TypeEW]
			
			dict1=db_collection.find_one({'PId': resultID}) #get data from male db	
			prod={}

			if (dict1!=None):
				prod={}
				for key,val in dict1.items():
					if (key!='featureVectors' and key!='textSearch' and key!='_id'): #cuz featureVectors are very long and output gets confusing
						prod[key]=val
						
						print(str(key)+ " : "+str(val))

				
			finalResult[product_count]=prod
			product_count+=1
		return finalResult

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

class Searcher:
	def search( queryFeatures,gender,typeEW, category,limit = 10):
		results = {}
		client = pymongo.MongoClient("mongodb+srv://zahra:passmongodb@cluster0.femwg.mongodb.net/test?retryWrites=true&w=majority")
	   
		
		if (gender=='F'): 
			Gender='Female'
		else:
			Gender='Male'
		db = client[Gender]
	 
		queryT = {'Category': {'$exists': 1},}
		projectionT = {'_id': 0, 'Category': 1}
		
		#query to get feature vectors
		queryFV = {'featureVectors': {'$exists': 1},}
		projectionFV = {'_id': 0, 'featureVectors': 1}
		
		
		brand_count=0
		print("Gender is: "+ Gender)
		print("Calculating distances..")
		
		db_collection=db[typeEW]
			
		
		
#             idd = list(db[Gender].find(query1, projection1)) #get id of the products
		typels=list(db_collection.find(queryT, projectionT))
		titles=[]
		types=[]
#             for dat in idd:
#                 for key,value in dat.items():
#                     titles.append(value) #store id in titles array to make accessing from db easy later on

		for type1 in typels:
			for key,value in type1.items():
				types.append(value) #store type of product in types array to retrieve type of products
		print(len(typels))


		products = list(db_collection.find(queryFV, projectionFV)) #access women portion of brand from db
		print(len(products))
		product_count=0
		for product in products: #iterate thru all products in db
			image_count=1
			id_val=""
			check_wrong=0
			for key, value in product.items():
				fVector=literal_eval(value) #convert string from db into list

				resultValue=1.2 #max distance value
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
#                 print(check_okay)
				if (check_okay==1):
#                     print("here???")
					for f in fVector:
					   
						if (check!=1): #check=1 means distance of FV of product is greater than 1.5 so skip remaining FV of same product
						   
							d = Searcher.chi2_distance(f, queryFeatures) #pass indices from feature vectors to calculate distance
							print(d)
							
							if (d>2): #if distance is greater than max value then don't loop further thru images
								check=1
								break;
							if d<resultValue:
								resultValue=d
					if (d<2): #if distance is less than 1.5 then store in results
						dict2=db_collection.find_one({'featureVectors':str(fVector)})
#                         print(dict2)
						results[dict2['PId']] = resultValue #store the distance of products with its title in dictionary
						
					else:
						break; #if distance is greater than 1.5, don't loop further

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

	

api.add_resource(SearchByImage,"/sbi/<string:imagePath>/<string:gender>")

if __name__=="__main__":
	app.run(debug=True,  port=5000)