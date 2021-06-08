brandList = ['Fiio', 'Samsung', 'POCO', 'Samsung']
modelList = ['M15', 'Galaxy', 'X3', 'Galaxy']
choicesList = []
n = 0
for brand in brandList:
    if brand != choicesList[0]:
        choicesList.append(brand)
        choicesList.append(modelList[n])
        n+=1
    else:
        choicesList.append(modelList[n])
        n+=1
print(choicesList)
