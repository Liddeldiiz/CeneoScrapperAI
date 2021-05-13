from app import app
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
                self.opinions.append(Opinion().extractOpinion(opinion))
            try:
                url = self.url_pre + extractElement(pageDOM, 'a.pagination__next', "href")
            except IndexError:
                url = None

    def productIDextraction(self):
        url = input()#"https://www.ceneo.pl/96961305#tab=reviews"

        fullURLList = url.split("https://www.ceneo.pl/")
        partURLList = fullURLList[1].split("#tab=reviews")
        productID = partURLList[0]
        print(productID)
        return productID

    def productNameExtraction(self):
        pass

    def extractOpinions(self, opinions):
        opinionsList = []
        for opinion in opinions:
            singleOpinion = {
                key:self.extractFeature(opinion, *args)
                for key, args in selectors.items()
            }
            singleOpinion["Opinion ID"] = opinion["data-entry-id"]
            opinionsList.append(singleOpinion)
        return opinionsList

    def exportProduct(self):
        with open("opinions/{}.json".format(self.productID), "w", encoding="UTF-8") as jf:
            json.dump(dict(self), jf, indent=4, ensure_ascii=False)

    def __str__(self):
        return '''productID: {}<br>
        name: {}<br>'''.format(self.productID, self.productName)+"<br>".join(str(opinion) for opinion in self.opinions)

    def __dict__(self):
        return {
            "productID": self.productID, 
            "name": self.productName,
            "opinoins": [dict(opinion) for opinion in self.opinions]
        }