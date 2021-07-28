from flask import Flask
from flask_restful import Api,Resource
import pymongo
from pymongo import MongoClient
from flask_cors import CORS
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import nltk
from nltk.stem import PorterStemmer

app=Flask(__name__)
api=Api(app)
CORS(app)


titles=[]
text=[]
MenBrands=['Cambridge','Outfitters','Jdot'] #men brands
men_idx=[0,0,0] #to store indices of each male brand to display products from db after text search
WomenBrands=['Limelight','khaadi','sapphire','Outfitters','Jdot'] #women brands
women_idx=[0,0,0,0,0] ##to store indices of each female brand to display products from db after text search
client = pymongo.MongoClient("mongodb+srv://zahra:passmongodb@cluster0.femwg.mongodb.net/test?retryWrites=true&w=majority")

query = {'textSearch': {'$exists': 1}}
projection = {'_id': 0,'textSearch':1}

query1 = {'PId': {'$exists': 1}}
projection1 = {'_id': 0, 'PId': 1}




class SearchByText(Resource):
	def get(self,searchInput,gender):
		Data=[] #to store all data from db
		IDs=[] #to store ids of products from db
		idx_arr=[] #to store indices of each brand to display products from db after text search. size will be 3 if men search and 5 if women search
		Brnads=[]



		s=0
		i=0

		(Data,IDs,idx_arr)=TextSearchGender(gender) #this function gets the data from db for the spcified gender



		#perform stemming on input data to achieve good results
		ps = PorterStemmer()
		arr=ConvertToList(searchInput) #convert user input to list
		inputsearch=""
		for v in arr:
		    inputsearch+=ps.stem(v) #perform stemming
		    inputsearch+=" "

		#specify the gender
		if (gender=='F'):
		    gender="Women"
		else:
		    gender="Men"


		titles=[]
		data=[]
		AllProducts={}
		# print(Data)
		# print(IDs)
		print(idx_arr)
		AllProducts=TextSearch(inputsearch,Data,IDs,gender,idx_arr) #perform textual search on the input

		for key,value in AllProducts.items(): #displaying all the resultant products
		    print(str(key)+": ")
		    print(value)

		


		return AllProducts #returning dictionary object that conatins all products



def ConvertToList(string): 
    li = list(string.split(" ")) 
    return li 

def TextSearchGender(gender): #this function returns textsearch for specified gender from db
    s=0 
    i=0
    titles=[]
    text=[]
    idx_array=[0,0]
    
    
    if (gender=='F'):
        db=client['Female'] #get specific gender from db
    else:
        db=client['Male'] #get specific gender from db
   
    s=0 
    i=0
    id_count=0
    category=["Eastern","Western"] #2 sub catgeories in db
    for c in category:
        
        if (c=='Eastern'):
            idx_array[0]=i
        elif (c=='Western'):
            idx_array[1]=i
       
        db_collection=db[c] #get specific gender of brand from db
 

        desc = list(db_collection.find(query, projection)) #all products from db in list form
        idd = list(db_collection.find(query1, projection1)) #IDs of all products from db in list form
        
        id_count=0
        for message in desc:
            for key, value in message.items():
                text.append(value) #store the textsearch data in text array
            i+=1
            id_count+=1

        k=0    
        for dat in idd:
            for key,value in dat.items():
                titles.append(value) #store the IDs of products in titles array
            if (k==id_count-1): #to ensure that text and titles have same length
                break;
            k+=1
            
    return (text,titles,idx_array) #return data,IDs, index array and brands to be used later on

    
def TextSearch(inputText,searchText,titles,gender,array_idx): #this function computes the textual search and retrieves results of search from db
    product_count=1 #for storing products in dictionary
    choices_dict = {idx: el for idx, el in enumerate(searchText)} #converts data to dictionary
    choices_titles = {idx: el for idx, el in enumerate(titles)} ##converts titles to dictionary
    fromdocs=process.extract(inputText, choices_dict,scorer=fuzz.token_set_ratio,limit=30) #apply fuzzy search. get Maximum of 30 products
#     print(process.extract(inputText, choices_dict,scorer=fuzz.token_set_ratio,limit=30))
  
#     print(array_idx)
    number=0
    dict1={}
    product={}
    LenArray=len(array_idx) #this tells us the total brands we'll be iterating. 3 for men. 5 for women
    
    if (gender=='Women'):
        db=client['Female']
    else:
        db=client['Male']
    
    for i in range (len(fromdocs)):
        number=fromdocs[i][2] #stores the index of resultant textSearch product
        accuracy=fromdocs[i][1] #stores accuracy of resultant textSearch product
#         print(str(number)+gender)

    

        #specify which index(number) does the product belong to and get relevant brand from db
        if (number>=array_idx[0]): #if value is greater then it belongs to Western Category
            db_collection=db['Western']
        else:
            db_collection=db['Eastern'] #if value is greater then it belongs to Eastern Category

       
        
       
        product=db_collection.find_one({'PId': titles[number]}) #get data from db
        
        
#         print(titles[number])


        prod={} #will contain each individual product
        if (product!=None): 
            for key,searchInput in product.items():
                if (key!='featureVectors' and key!='textSearch'and key!='_id' and accuracy>65): #add every other value except for these in our prod dictionary and only if accuracy of search result is greater than 65
                    prod[key]=searchInput
#                 if (key!='featureVectors' and accuracy>65):
#                     print(str(key)+ " : "+str(searchInput))
            

        if (len(prod)!=0): #if product exists, only then add in dict1(all products)
            dict1[product_count]=prod
            product_count+=1
           
    return dict1 #returns dictionary containing all products of text search
        

api.add_resource(SearchByText,"/sbt/<string:searchInput>/<string:gender>")

if __name__=="__main__":
	app.run(debug=True, port=5001)