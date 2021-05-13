from app import app
from app.models.opinion import Opinion
from app.models.product import Product
from app.forms import ProductForm
from flask import request, render_template, redirect, url_for
import requests
import json

@app.route('/')
@app.route('/index')
def index():
    opinion1 = Opinion()
    return str(opinion1)

@app.route('/example/<var>')
def example(var):
    pass

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    form = ProductForm()
    if request.method == 'POST' and form.validate():
        product = Product(request.form['productID'])
        respons = requests.get(product.opinionsPageURL())
        if respons.status_code == 200:
            product.extractProduct()
            product.exportProduct()
            return redirect(url_for('product', productID=product.productID))
        else:
            form.productID.errors.append("For given product ID there is no product")
    return render_template('extract.html', form=form)

#HOMEWORK: Analyze the function above!!!

@app.route('/product/<productID>')
def product(productID):
    return "You are now on the product page"

@app.route('/productList')
def productList():
    return "You are now on the product list page"

@app.route('/author')
def author():
    return "Applied informatics 2020/2021"