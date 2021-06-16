from app import app
from app.models.opinion import Opinion
from app.models.product import Product
from app.forms import ProductForm
from app.forms import SelectForm
from flask import request, render_template, redirect, url_for, jsonify
from os import listdir
import requests
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
from matplotlib import pyplot as plt
import os

from app.models.selection import choicesList

from tinydb import Query
from app.models.product import db

#from flask_sqlalchemy import SQLAlchemy

# common bug is: RuntimeError: main thread is not in main loop
# UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
# fig = self.plt.figure(figsize=self.figsize)


app.config['SECRET_KEY'] = "NotSoSpecialSecretKey"


@app.route('/')
@app.route('/index')
def index():
    requirements = []
    with open("requirements.txt") as f:
        line = f.readline()
        while line:
            line = f.readline()
            requirements.append(line)
    return render_template('main.html.jinja', requirements=requirements)

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    form = ProductForm()
    if request.method == 'POST' and form.validate_on_submit():
        product = Product(request.form['productID'])
        respons = requests.get(product.opinionsPageURL())
        if respons.status_code == 200:
            product.extractProduct()
            product.countProductStatistics()
            product.exportProduct()
            return redirect(url_for('extractedProduct', productID=product.productID))
        else:
            form.productID.errors.append("For given product ID there is no product")
    return render_template('extract.html.jinja', form=form)

@app.route('/extractedProduct/<productID>')
def extractedProduct(productID):
    #print(productID)
    product = Product(productID)
    #print(product)
    #opinions = product.importProduct().opinionsToDataFrame()
    opinions = product.importProductFromDB().opinionsToDataFrame()
    #print("Product var in def extractedProduct:", product)
    #product.createGraphs()
    #tables=[opinions.to_html(classes='table table-striped table-sm table-responsive display', table_id="opinions")]
    return render_template('extractedProduct.html.jinja', tables=[opinions.to_html(classes='table table-striped table-sm table-responsive display', table_id="opinions")])

@app.route('/product/<productBrand>/<product>')
def product(productBrand, product):
    productID = product.split()[1]
    print("print in terminal works")
    #print(productID)

    productToImport = Product(productID)
    #print(productToImport)
    opinions = productToImport.importProductFromDB().opinionsToDataFrame()
    #print("Product var in def product:", product)
    #with open("app/opinions/{}/{}.json".format(productBrand, product), encoding="cp437", errors="ignore") as f:
    #    d = json.load(f)
    
    #opinions = json_normalize(d['opinions'])
    stars = opinions['stars'].value_counts().sort_index(ascending=True).reindex(np.arange(0, 5.5, 0.5).tolist(), fill_value=0)
    

    redomendations = opinions['recomendation'].value_counts(dropna=False)
    averageScore = opinions['stars'].mean()
    prosCount = opinions['advantages'].count()
    consCount = opinions['disadvantages'].count()
    purchased = opinions['purchaseDate'].count()
    advantages = []
    for a in opinions['advantages'].dropna().tolist():
        advantages += a.split(', ')
    pros = pd.Series(advantages, name="advantages").value_counts()
    disadvantages = []
    for a in opinions['disadvantages'].dropna().tolist():
        disadvantages += a.split(', ')
    cons = pd.Series(disadvantages, name="disadvantages").value_counts()
    features = pros.to_frame().join(cons)

    """data = [
        
        ("01-01-2020", 1597),
        ("02-01-2020", 1456),
        ("03-01-2020", 1908),
        ("04-01-2020", 896),
        ("05-01-2020", 755),
        ("06-01-2020", 453),
        ("07-01-2020", 1100),
        ("08-01-2020", 1235),
        ("09-01-2020", 1478),
        
    ]

    labels = [row[0] for row in data]
    values = [row[1] for row in data]"""

    
    #labels = [row[0] for row in stars]
    #values = [row[1] for row in stars]
    print(stars)
    
    
    
    return render_template('product.html.jinja', productBrand=productBrand, product=product, tables=[opinions.to_html(classes='table table-striped table-sm table-responsive', table_id="opinions")],
    stars=stars, 
    redomendations=redomendations, 
    averageScore=averageScore,
    prosCount=prosCount, 
    consCount=consCount,
    purchased=purchased,
    features=features,
    #labels=labels,
    #values=values, 
    productID=productID)

@app.route('/brands/<productBrand>/<products>')
def brands(productBrand, products):
    #return "you have reached the brand page"

    return render_template('brands.html.jinja', productBrand=productBrand, products=products)

@app.route('/products', methods=['GET', 'POST'])
def products():
    form = SelectForm()
    
    #brandList = [x.split(".")[0] for x in listdir("app/opinions")]
    for x in range(0, len(choicesList)):
        if x%2 != 0:
            choicesList[x] = list(choicesList[x])
    if request.method == 'POST':
        brandIndex = int(request.form['brand'])
        productBrand = choicesList[brandIndex]
        productsIndex = int(request.form['products'])
        #print("This is the choicesList:", choicesList)
        products = choicesList[productsIndex]
        #print("These are the products:", products)
        productDB = Query()
        DB_Products_model = []
        counter = 0
        for item in products:
            result = db.search(productDB.model == item)
            while counter < len(result):
                #print(result[counter]['model'])
                #print(result[counter]['productID'])
                DB_Products_model_ID = result[counter]['model'] + " " + result[counter]['productID']
                DB_Products_model.append(DB_Products_model_ID)
                counter+=1
        #print(DB_Products_model)
        return render_template('brands.html.jinja', productBrand=productBrand, DB_Products_model=DB_Products_model)

    return render_template('products.html.jinja', form=form, choicesList=choicesList)

@app.route('/author')
def author():
    return render_template('author.html.jinja')

# task: prepare about author page