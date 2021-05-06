from app import app
from app.utils import extractElement

class opinion:

    selectors = {
        "Author":  ["span.user-post__author-name"] ,
        "Recomendation":  ["span.user-post__author-recomendation > em"],
        "Stars":  ["span.user-post__score-count"],
        "Content": ["div.user-post__text"],
        "Advantages": ["div.review-feature__col:has(> div[class*=\"positives\"])"],
        "Disadvantages":  ["div.review-feature__col:has(> div[class*=\"negatives\"])"],
        "Helpful":  ["button.vote-yes > span"],
        "Unhelpful": ["button.vote-no > span"],
        "Publish Date": ["span.user-post__published > time:nth-child(1)", "datetime"],
        "Purhcase Date": ["span.user-post__published > time:nth-child(2)", "datetime"]
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
            setattr(self, key, extractElement(opinionTree, *values))
        self.opinionID = opinionTree["data-entry-id"]
        self.transformOpinion()

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

    def __str__(self):
        pass