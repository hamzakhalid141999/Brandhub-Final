#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[5]:


import glob
import numpy as np
import cv2
import os
IMG_SIZE=60
CATEGORIES = ["Full", "NFull"]
def computeCategory(imagePath,model):
#     filename = 'finalized_model.sav'
#     print(filename)
#     model = pickle.load(open(filename, 'rb'))
    files = glob.glob(imagePath)
    path="BrandHub/queries"
    print(files)
    i=0
    x=[]
    filenames=[]
    for myFile in files:
        filenames.append(myFile)
        image = cv2.imread(myFile,cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image,(IMG_SIZE,IMG_SIZE))
        x.append(image)
        
        X_data=np.array(x)
        X_data = X_data.reshape((-1, IMG_SIZE, IMG_SIZE, 1))
        X_data = X_data/ 255.0
        p = model.predict(X_data)
        print(p)
        label = CATEGORIES[int(np.round(p[0]))]
        print(label)
        return label

