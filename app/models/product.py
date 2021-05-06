from app import app
from app.utils import extractElement
from app.models.opinion import extractOpinion, transformOpinion
import requests
from bs4 import BeautifulSoup

class product:

    url_pre = 'https://www.ceneo.pl'
    url_post = '#tab=reviews'

    def __init__(self, productID=None, productName=None, opinions=[]):
        self.productID = productID
        self.productName = productName
        self.opinions = opinions

    def extractProduct(self):
        url =  self.url_pre + '/' + self.productID + self.url_post

        while url:
            respons = requests.get(url)
            pageDOM = BeautifulSoup(respons.text, 'html.parser')
            opinions = pageDOM.select("div.js_product-review")
            for opinion in opinions:
                self.opinions.append(Opinion().extractOpinion(opinion).)
            try:
                url = self.url_pre + extractElement(pageDOM, 'a.pagination__next', "href")
            except IndexError:
                url = None

        opinionsDF = pd.DataFrame.from_dict(opinionsList)
        opinionsDF
        print(opinionsDF)

        transformOpinions(opinionsList)

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


    def __str__(self):
        pass