#!/usr/bin/env python
# coding: utf-8

# In[5]:


import glob
import numpy as np
import cv2
import os
IMG_SIZE=60
CATEGORIES = ["top", "bottom"]

def computeCategory(imagePath,model):
    files = glob.glob(imagePath)
    print(files) #displays query file name
    i=0
    x=[]
    filenames=[]
    for myFile in files:
        filenames.append(myFile) #append image in array
        image = cv2.imread(myFile,cv2.IMREAD_GRAYSCALE) #read image and convert into black & white
        image = cv2.resize(image,(IMG_SIZE,IMG_SIZE)) #resize image to 60x60
        x.append(image) #append resized image in array
        
        X_data=np.array(x) #convert array that contains image to numpy array for prediction
        X_data = X_data.reshape((-1, IMG_SIZE, IMG_SIZE, 1)) #-1 is for features, resize image to 60x60, 1 is for grayscale
        X_data = X_data/ 255.0 #scale data by dividing by max value
        p = model.predict(X_data) #pass the image to the model for prediction
        print(p)
        label = CATEGORIES[int(np.round(p[0]))] # 0=top, 1=bottom. Round the float and convert to into to get either 0 or 1
        print(label)
        return label #return predicted label


# In[ ]:





# In[ ]:




