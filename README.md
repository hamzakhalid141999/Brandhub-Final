BrandHub is an online application that connects the world of shopping with all the brands
at one place. One can search their favorite clothing items, make comparisons and choose
the best products on one platform! This app is all about saving the time that you spend on browsing and searching for items of
your choice. This project combines various technical challenges such as Web scraping,
image detection, object detection, data analysis and recommendation engine.

<<<<<<< HEAD
We've used Flask JS API for communication of data between our UI, which is React JS, and
the Python backend scripts, which process the query through the required algorithm, by
fetching the required data from MongoDB. So React and Flask doesn't has to interact with
MongoDB, python scripts maintain a standalone relationship. If there will be required, a
direct communication between React and Mongo DB, Express JS will be used, hence the 
MERN stack will be deployed. 


=======
MANUAL:
CleanData.ipynb file cleans the data of all products and stores a cleaned data string back in MongoDB for all products. This string is later used for Search By Text
TopBottom.ipynb is our model that detects whether an image is a top or bottom. This file trains our data
Topbottom1.py predicts whether a given image is a top or bottom. It uses the model trained TopBottom.ipynb
WebScraping.ipynb scrapes all the websites and stores their data in MongoDB

