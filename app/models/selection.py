from tinydb import Query
from app.models.product import db
import json


choicesList = []
models = []
with open("db.json", "r", encoding="UTF-8") as jf:
    product = json.load(jf)
    descriptiveList = []
    n = 1
    while n <= len(product["_default"]):
        name = product["_default"][str(n)]['Brand']
        descriptiveList.append(name)
        n+=1
descriptiveList_set = set(descriptiveList)
productDB = Query()
    #for item in descriptiveList_set:
    #   result = db.search(productDB.Brand == "model")
    #    choicesList.append(item, (result))
for item in descriptiveList_set:
    result = db.search(productDB.Brand == item)
    n = 0
    models.clear()# I need to find a way to clear the models list before it appends the previous models to another brand...
    while n < (len(result)):
        #print(result[0]["model"])
        models.append(result[0]["model"])
        n+=1
    models_set = set(models)
    choicesList.append(item)
    choicesList.append(models_set)
print(choicesList)
n=0
#print(choicesList)
