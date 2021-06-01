from app import app
from app.models.opinion import Opinion
from app.models.product import Product
from app.forms import ProductForm
from flask import request, render_template, redirect, url_for
from os import listdir
import requests
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
from matplotlib import pyplot as plt
import os


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
            return redirect(url_for('extractedProduct', productID=product.productID))
        else:
            form.productID.errors.append("For given product ID there is no product")
    return render_template('extract.html.jinja', form=form)

@app.route('/extractedProduct/<productID>')
def extractedProduct(productID):
    return render_template('extractedProduct.html.jinja', productID=productID)

@app.route('/product/<productBrand>/<productID>')
def product(productBrand, productID):
    """try:
        with open("app/opinions/{}/{}.json".format(productBrand, productID), encoding="cp437", errors="ignore") as f:
            d = json.load(f)
    
        opinions = json_normalize(d['opinions'])
        stars = opinions["stars"].value_counts().sort_index(ascending=True).reindex(np.arange(0, 5.5, 0.5).tolist(), fill_value=0)
        ax = stars.plot.bar(color="lightskyblue")
        ax.set_title("Frequency of stars in opinons")
        ax.set_xlabel("Stars values")            
        ax.set_ylabel("Number of opinions")
        plt.savefig('app/ststic/Graphs/{}/{}/stars.png'.format(productBrand, productID))
    except OSError:
        parent_dir_graphs = "D:\\Applied_informatics\\CeneoScrapperAI\\app\\static\\Graphs"
        path = os.path.join(parent_dir_graphs, productBrand)
        os.mkdir(path)
        with open("app/opinions/{}/{}.json".format(productBrand, productID), encoding="cp437", errors="ignore") as f:
            d = json.load(f)
        opinions = json_normalize(d['opinions'])
        stars = opinions["stars"].value_counts().sort_index(ascending=True).reindex(np.arange(0, 5.5, 0.5).tolist(), fill_value=0)
        ax = stars.plot.bar(color="lightskyblue")
        ax.set_title("Frequency of stars in opinons")
        ax.set_xlabel("Stars values")
        ax.set_ylabel("Number of opinions")
        plt.savefig('app/ststic/Graphs/{}/{}/stars.png'.format(productBrand, productID))
    #ax.set_title("Frequency of stars in opinons")
    #ax.set_xlabel("Stars values")
    #ax.set_ylabel("Number of opinions")
    """
    with open("app/opinions/{}/{}.json".format(productBrand, productID), encoding="cp437", errors="ignore") as f:
        d = json.load(f)
    
    opinions = json_normalize(d['opinions'])
    stars = opinions['stars']

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
    
    return render_template('product.html.jinja', 
    stars=stars, 
    redomendations=redomendations, 
    averageScore=averageScore,
    prosCount=prosCount, 
    consCount=consCount,
    purchased=purchased,
    features=features,
    productBrand=productBrand, 
    productID=productID)

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