from app import app # app module not importing into this file
from app.utils import extractElement
from app.models.opinion import Opinion
import requests
import json
from bs4 import BeautifulSoup

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
            for opinion in opinions:
                self.opinions.append(Opinion().extractOpinion(opinion).transformOpinion())
            try:
                url = self.url_pre + extractElement(pageDOM, 'a.pagination__next', "href")
            except TypeError:
                url = None

    def exportProduct(self):
        with open("app/opinions/{}.json".format(self.productID), "w", encoding="UTF-8") as jf:
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