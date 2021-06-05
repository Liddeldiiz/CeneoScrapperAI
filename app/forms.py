from numpy import array
from wtforms import StringField, SubmitField, validators
from flask_wtf import FlaskForm
from wtforms.fields.core import SelectField

from os import listdir
import json
from tinydb import TinyDB, Query

from app.models.product import db

from pandas import json_normalize

class ProductForm(FlaskForm):
    productID = StringField(
        'Enter product ID',
        [
            validators.DataRequired(message = "Please enter product ID"),
            validators.Length(min=8, max=9, message = "Product ID must have 8 characters"),
            validators.Regexp(regex="^[0-9]+$", message="Product ID can contain only 9 digits")# there are product ID longer then 8 digits, how to change this validator?
        ])
    submit = SubmitField('Extract')

class Form(FlaskForm):
    with open("db.json", "r", encoding="UTF-8") as jf:
        product = json.load(jf)
        brandList = []
        n = 1
        while n <= len(product["_default"]):
            name = product["_default"][str(n)]['name']
            brandList.append(name)
            n+=1
        print(brandList)
        #opinions = json_normalize(product["opinions"])
    

    brand = SelectField('brand', choices=[brandList]) # ==> ((brand, (productList from brand)), brand#2, (productList from brand#2))
    products = SelectField('product', choices=[])
    
    #(brandsList[0], productList[0]), (brandsList[1], productList[1]), (brandsList[2], productList[2]), (brandsList[3], productList[3]), (brandsList[4], productList[4])