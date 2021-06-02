from app import app # app module not importing into this file
from app.utils import extractElement

class Opinion:

    selectors = {
        "author":  ["span.user-post__author-name"] ,
        "recomendation":  ["span.user-post__author-recomendation > em"],
        "stars":  ["span.user-post__score-count"],
        "content": ["div.user-post__text"],
        "advantages": ["div.review-feature__col:has(> div[class*=\"positives\"])"],
        "disadvantages":  ["div.review-feature__col:has(> div[class*=\"negatives\"])"],
        "helpful":  ["button.vote-yes > span"],
        "unhelpful": ["button.vote-no > span"],
        "publishDate": ["span.user-post__published > time:nth-child(1)", "datetime"],
        "purchaseDate": ["span.user-post__published > time:nth-child(2)", "datetime"]
    }

    def __init__(self, opinionID=None, author=None, recomendation=None, stars=None, content=None, advantages=None, disadvantages=None, helpful=None, unhelpful=None, publishDate=None, purchaseDate=None):
        self.opinionID = opinionID
        self.author = author
        self.recomendation = recomendation
        self.stars = stars
        self.content = content
        self.advantages = advantages
        self.disadvantages = disadvantages
        self.helpful = helpful
        self.unhelpful = unhelpful
        self.publishDate = publishDate
        self.purchaseDate = purchaseDate

    def extractOpinion(self, opinionTree):
        for key, value in self.selectors.items():
            setattr(self, key, extractElement(opinionTree, *value))
        self.opinionID = opinionTree["data-entry-id"]
        #self.transformOpinion()
        return self

    def transformOpinion(self):
        try: 
            self.advantages = self.advantages.replace("Zalety\n", "").replace("\n", ", ")
        except AttributeError:
            pass
        try:
            self.disadvantages = self.disadvantages.replace("Wady\n", "").replace("\n", ", ")
        except AttributeError:
            pass
        self.recomendation = True if self.recomendation == "Polecam" else False if self.recomendation == "Nie polecam" else None
        self.stars = float(self.stars.split("/")[0].replace(",", "."))
        self.content = self.content.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        self.helpful = int(self.helpful)
        self.unhelpful = int(self.unhelpful)
        return self

    def __str__(self):
        return 'opinionID: '+str(self.opinionID)+'<br>'+'<br>'.join(key+": "+str(getattr(self, key)) for key in self.selectors.keys())

    def toDict(self):
        return {'opinionID': self.opinionID} | {key: getattr(self, key) for key in self.selectors.keys()}
        

