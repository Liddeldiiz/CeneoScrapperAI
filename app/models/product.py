from app import app # app module not importing into this file
from app.utils import extractElement
from app.models.opinion import Opinion
import requests
import json
from bs4 import BeautifulSoup
import os

class Product:

    url_pre = 'https://www.ceneo.pl'
    url_post = '#tab=reviews'

    def __init__(self, productID=None, productName=None, opinions=[]):
        self.productID = productID
        self.productName = productName
        self.opinions = opinions

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

    def exportProduct(self):
        directory = self.productName.split()[0]
        directoryVar = len(directory)+1
        productModel = self.productName[directoryVar:]
        # EAFP - Easier to Ask for Forgivness than Permission
        try:
            productModel = productModel.replace('/', '-')
        except AttributeError:
            pass

        try:
            with open("app/opinions/{}/{}.json".format(directory, productModel + "_" + self.productID), "w", encoding="UTF-8") as jf:
                json.dump(self.toDict(), jf, indent=4, ensure_ascii=False)
        except OSError:
            parent_dir = "D:\\Applied_informatics\\CeneoScrapperAI\\app\\opinions"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            with open("app/opinions/{}/{}.json".format(directory, productModel + "_" + self.productID), "w", encoding="UTF-8") as jf:
                json.dump(self.toDict(), jf, indent=4, ensure_ascii=False)

    def __str__(self):
        return '''productID: {}<br>
        name: {}<br>'''.format(self.productID, self.productName)+"<br>".join(str(opinion) for opinion in self.opinions)

    def toDict(self):
        return {
            "productID": self.productID, 
            "name": self.productName,
            "opinoins": [opinion.toDict() for opinion in self.opinions]
        }