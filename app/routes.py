from app import app
from app.models.opinion import Opinion
from app.models.product import Product
from app.forms import ProductForm
from flask import request, render_template, redirect, url_for
from os import listdir
import requests
import json

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

@app.route('/product/<productID>')
def product(productID):
    return render_template('product.html.jinja', productID=productID)

@app.route('/products')
def products():
    productsList = [x.split(".")[0] for x in listdir("app/opinions")]
    return render_template('products.html.jinja', productsList=productsList)

@app.route('/author')
def author():
    return "Applied informatics 2020/2021"

# task: when we click on the products button, you will have the page and there will be all the products that we have extracted
#list group bootstrap