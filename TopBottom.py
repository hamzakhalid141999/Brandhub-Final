#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from tqdm import tqdm
import random

DATADIR = "C:/Users/dell/Desktop/New folder"

CATEGORIES = ["top", "bottom"] 

training_data = []
IMG_SIZE=60

def create_training_data():
    for category in CATEGORIES:  # iterate over categories

        path = os.path.join(DATADIR,category)  # create path to top and bottom
        class_num = CATEGORIES.index(category)  # get the classification  (0 or a 1). 0=top 1=bottom

        for img in tqdm(os.listdir(path)):  # iterate over each image per top and bottom
            try:
                img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)  # convert to array
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
                training_data.append([new_array, class_num])  # add this to our training_data
            except Exception as e:  #handle any exception
                pass
                
           

create_training_data() #store training data

print(len(training_data)) #print len of training data
random.shuffle(training_data) #shuffle training data


# In[2]:


X = [] #features
y = [] #lables

#store features(images) and label in X and y respectively
for features,label in training_data:
    X.append(features)
    y.append(label)
    
X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1) # -1 represents how many features we have ,resize images to 60x60, 1 is because of grayscale


# In[8]:


import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow import keras
import pickle

def trainModel(X,y):
    X = np.array(X/255.0) #scale data by dividing with max value and convert to numpy array
    y=np.array(y)

    model = Sequential() 

    #add 2 convolutional layers
    model.add(Conv2D(64, (3, 3), input_shape=X.shape[1:])) # 1: means we ignore the -1 in -1x60x60x1 because that doesn't contribute to shape of images 
    model.add(Activation('relu')) #Rectified Linear Unit Activation
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3))) #filter of 64 with 3x3 kernel
    model.add(Activation('relu')) #Rectified Linear Unit Activation
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())  # convert 3D feature maps to 1D feature vectors

    model.add(Dense(64)) #adding a dense layer with 64 neurons

    model.add(Dense(1)) #final dense layer with 1 neuron to get 1 value
    model.add(Activation('sigmoid')) #gives values between 0 and 1
    #we use binary cross entropy cuz we have 2 categories
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy']) #use binray cross entropy as we have 2 classes
    
   
    model.fit(X, y, batch_size=32, epochs=10, validation_split=0.3) #test on 30% of data
    model.save('TopBottom_model') #save model in this folder to be used later on
    loaded_model=keras.models.load_model("TopBottom_model") #load the saved model
    np.testing.assert_allclose(model.predict(X),loaded_model.predict(X)) #check if the saved and loaded model are same. If no exception, it means they're same
   
    
     
    


# In[9]:


trainModel(X,y) #pass features and labels for training


# In[ ]:




