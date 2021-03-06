from app import app # app module not importing into this file
from app.utils import extractElement
from app.models.opinion import Opinion
from bs4 import BeautifulSoup
from pandas import json_normalize
import pandas as pd
import requests
import json
import os
import numpy as np
import glob

from tinydb import TinyDB, Query
db = TinyDB('db.json')

#from matplotlib import pyplot as plt

class Product:

    url_pre = 'https://www.ceneo.pl'
    url_post = '#tab=reviews'

    def __init__(self, productID=None, productName=None, directory=None, productModel=None, opinions=[], averageScore=None, opinionsCount=None, prosCount=None, consCount=None):
        self.productID = productID
        self.productName = productName
        self.directory = directory
        self.productModel = productModel
        self.opinions = opinions.copy()
        self.averageScore = averageScore
        self.opinionsCount = opinionsCount
        self.prosCount = prosCount
        self.consCount = consCount

    def opinionsPageURL(self):
        return self.url_pre + '/' + self.productID + self.url_post


    def extractProduct(self):
        url =  self.opinionsPageURL()

        while url:
            respons = requests.get(url)
            pageDOM = BeautifulSoup(respons.text, 'html.parser')
            opinions = pageDOM.select("div.js_product-review")

            self.productName = pageDOM.select('div.js_searchInGoogleTooltip')[0].text.strip()
            for opinion in opinions:
                self.opinions.append(Opinion().extractOpinion(opinion).transformOpinion())
            try:
                url = self.url_pre + extractElement(pageDOM, 'a.pagination__next', "href")
            except TypeError:
                url = None
        
    def countProductStatistics(self):
        opinions = self.opinionsToDataFrame()
        self.averageScore = opinions['stars'].mean()
        self.opinionsCount = len(self.opinions)
        self.prosCount = opinions['advantages'].count()
        self.consCount = opinions['disadvantages'].count()
        


    def exportProduct(self):
        # EAFP - Easier to Ask for Forgivness than Permission
        print("exportProduct, productName: ", self.productName)
        self.directory = self.productName.split()[0]
        directoryVar = len(self.directory)+1
        self.productModel = self.productName[directoryVar:]
        #productName = self.productName.split()[1]
        #brand = self.productName.split()[0]
        #print(self.productID)
        try:
            self.productModel = self.productModel.replace('/', '-') # If the product name contains "/" such a symbol at can be interpreted by the progam as a directory backslash?
        except AttributeError:
            pass

        try:
            with open("app/opinions/{}/{}.json".format(self.directory, self.productModel + "_" + self.productID), "w", encoding="UTF-8") as jf:
                json.dump(self.toDict(), jf, indent=4, ensure_ascii=False)
        except OSError:
            parent_dir_opinions = "D:\\Applied_informatics\\CeneoScrapperAI\\app\\opinions"
            path = os.path.join(parent_dir_opinions, self.directory)
            os.mkdir(path)
            with open("app/opinions/{}/{}.json".format(self.directory, self.productModel + "_" + self.productID), "w", encoding="UTF-8") as jf:
                json.dump(self.toDict(), jf, indent=4, ensure_ascii=False)
        return self

    
    def importProduct(self):
        for file in glob.glob(f'app/opinions/**/*{self.productID}.json', recursive=True):
            path = file
        self.productName = path.split("\\")[2].split(".")[0]
        self.directory = path.split("\\")[1]

        with open("app/opinions/{}/{}.json".format(self.directory, self.productName), "r", encoding="UTF-8") as jf:
            product = json.load(jf)
            self.productName = product['name']
            opinions = product["opinions"]
            for opinion in opinions:
                self.opinions.append(Opinion(**opinion))

        return self

    def importProductFromDB(self):
        for file in glob.glob(f'app/opinions/**/*{self.productID}.json', recursive=True):
            path = file
        self.productName = path.split("\\")[2].split(".")[0]
        self.directory = path.split("\\")[1]
        brand = self.productName.split()[0]
        print("The brand is:", brand)
        brandModel = self.productName.split()[1]
        #print("The model is:", brandModel)
        self.productModel = brandModel
        self.productName = brand

        
        tempProduct = Query()
        #print("Data Base has", len(db) ,"objects")
        #print("This is the productID in the importProductFromDB function:", self.productID)
        #tempResult = db.search(product.productID == "94882813")
        result = db.search(tempProduct.productID == self.productID)
        self.productName = result[0]['Brand']
        opinions = result[0]['opinions']
        #print(opinions[0])
        for opinion in opinions:
            self.opinions.append(Opinion(**opinion))
        
        return self
        
        
        

    def createGraphs(self):
        tempProduct = Query()
        result = db.search(tempProduct.productID == self.productID)
        #for file in glob.glob(f'app/opinions/**/*{self.productID}.json', recursive=True):
        #    path = file
        #self.productName = path.split("\\")[2].split(".")[0]
        #self.directory = path.split("\\")[1]

        #with open("app/opinions/{}/{}.json".format(self.directory, self.productName), "r", encoding="UTF-8") as jf:
        product = result[0]
        self.name = product['model']
        self.directory = product['Brand']
        opinions = json_normalize(product["opinions"])
        print(opinions)
        print(opinions['stars'])
        if os.path.isdir('app/static/Graphs/{}/{}'.format(self.directory, self.name)) == True:
            stars = opinions["stars"].value_counts().sort_index(ascending=True).reindex(np.arange(0, 5.5, 0.5).tolist(), fill_value=0)
            ax = stars.plot.bar(color="lightskyblue")
            ax.set_title("Frequency of stars in opinons")
            ax.set_xlabel("Stars values")
            ax.set_ylabel("Number of opinions")
            #plt.savefig('app/static/Graphs/{}/{}/stars.png'.format(self.directory, self.name))
        else:
            parent_dir_graphs = "app/static/Graphs"
            path = os.path.join(parent_dir_graphs, self.directory, self.name)
            os.makedirs(path)
                    
            stars = opinions["stars"].value_counts().sort_index(ascending=True).reindex(np.arange(0, 5.5, 0.5).tolist(), fill_value=0)
            ax = stars.plot.bar(color="lightskyblue")
            ax.set_title("Frequency of stars in opinons")
            ax.set_xlabel("Stars values")
            ax.set_ylabel("Number of opinions")
            #plt.savefig('app/static/Graphs/{}/{}/stars.png'.format(self.directory, self.name))
        return self


    def __str__(self):
        return '''productID: {}<br>
        name: {}<br>'''.format(self.productID, self.productName)+"<br>".join(str(opinion) for opinion in self.opinions)

    def toDict(self):
        tempProduct = Query()
        brand = self.productName.split()[0]
        brandModel = self.productName.split()[1]
        if db.search(tempProduct.productID == self.productID) == []:
            print("updating DataBase")
            print(self.productName, self.productModel)
            return db.insert({
                    "productID": self.productID, 
                    "Brand": brand,
                    "model": brandModel,
                    "opinions": [opinion.toDict() for opinion in self.opinions]
                })
        else:
            print("update feature not introduced yet")


    def opinionsToDataFrame(self):
        opinions = pd.json_normalize([opinion.toDict() for opinion in self.opinions]) # <-- list comprehension
        return opinions

    