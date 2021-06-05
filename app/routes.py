from app import app
from app.models.opinion import Opinion
from app.models.product import Product
from app.forms import ProductForm
from app.forms import Form
from flask import request, render_template, redirect, url_for, jsonify
from os import listdir
import requests
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
from matplotlib import pyplot as plt
import os

#from flask_sqlalchemy import SQLAlchemy

# common bug is: RuntimeError: main thread is not in main loop
# UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
# fig = self.plt.figure(figsize=self.figsize)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = "NotSoSpecialSecretKey"

# db = dataBase

# db = SQLAlchemy(app)

"""class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    brand_id = db.Column(db.Integer)"""

@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html.jinja')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    form = ProductForm()
    if request.method == 'POST' and form.validate_on_submit():
        product = Product(request.form['productID'])
        respons = requests.get(product.opinionsPageURL())
        if respons.status_code == 200:
            product.extractProduct()
            product.exportProduct()
            return redirect(url_for('extractedProduct', productID=product.productID))
        else:
            form.productID.errors.append("For given product ID there is no product")
    return render_template('extract.html.jinja', form=form)

@app.route('/extractedProduct/<productID>')
def extractedProduct(productID):
    product = Product(productID)
    opinions = product.importProduct().opinionsToDataFrame()
    product.createGraphs()
    product.importProductFromDB()

    return render_template('extractedProduct.html.jinja', tables=[opinions.to_html(classes='table table-striped table-sm table-responsive display', table_id="opinions")])

@app.route('/product/<productBrand>/<productID>')
def product(productBrand, productID):
    with open("app/opinions/{}/{}.json".format(productBrand, productID), encoding="cp437", errors="ignore") as f:
        d = json.load(f)
    
    opinions = json_normalize(d['opinions'])
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
    
    return render_template('product.html.jinja', 
    stars=stars, 
    redomendations=redomendations, 
    averageScore=averageScore,
    prosCount=prosCount, 
    consCount=consCount,
    purchased=purchased,
    features=features,
    #labels=labels,
    #values=values,
    productBrand=productBrand, 
    productID=productID)

@app.route('/brands/<productBrand>')
def brands(productBrand):
    #return "you have reached the brand page"
    productsList = [x.split(".")[0] for x in listdir("app/opinions/{}".format(productBrand))]
    return render_template('brands.html.jinja', productsList=productsList, productBrand=productBrand)

@app.route('/products', methods=['GET', 'POST'])
def products():
    form = Form()
    brandList = [x.split(".")[0] for x in listdir("app/opinions")]

    return render_template('products.html.jinja', form=form, brandList=brandList)

@app.route('/author')
def author():
    return render_template('author.html.jinja')

# task: prepare about author page