from app import app
from app.models.opinion import Opinion
from app.models.product import Product
from app.forms import ProductForm
from flask import request, render_template, redirect, url_for
from os import listdir
import requests
import json
import pandas as pd
import numpy as np


app.config['SECRET_KEY'] = "NotSoSpecialSecretKey"

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
            return redirect(url_for('product', productID=product.productID))
        else:
            form.productID.errors.append("For given product ID there is no product")
    return render_template('extract.html.jinja', form=form)

@app.route('/product/<productBrand>/<productID>')
def product(productBrand, productID):
    file = pd.read_json("app/opinions/{}/{}.json".format(productBrand, productID), encoding="utf-8")
    stars = None
    for i in file["opinions"]:
        stars += i["stars"]     # NOT QUIET SURE HOW TO COUNT THE DIFFERENT VALUES OF STARS
    
        #ax = stars.plot.bar(color="lightskyblue")
        #ax.set_title("Frequency of stars in opinons")
        #ax.set_xlabel("Stars values")
        #ax.set_ylabel("Number of opinions")
    #file_loaded = pd.read_json(file)
    #file_loaded.to_csv(r'app/opinions/{}/{}.csv'.format(productBrand, productID), index = None)
    #opinions = pd.read_csv(f"app/opinions/{productBrand}/{productID}.csv", sep=";", decimal=",", index_col=0)
    return render_template('product.html.jinja', i=i, productBrand=productBrand, productID=productID)

@app.route('/brands/<productBrand>')
def brands(productBrand):
    #return "you have reached the brand page"
    productsList = [x.split(".")[0] for x in listdir("app/opinions/{}".format(productBrand))]
    return render_template('brands.html.jinja', productsList=productsList, productBrand=productBrand)

@app.route('/products')
def products():
    brandList = [x.split(".")[0] for x in listdir("app/opinions")]
    return render_template('products.html.jinja', brandList=brandList)

@app.route('/author')
def author():
    return "Applied informatics 2020/2021"

# task: when we click on the products button, you will have the page and there will be all the products that we have extracted
#list group bootstrap