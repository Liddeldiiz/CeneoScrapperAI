from numpy import array
from wtforms import StringField, SubmitField, validators
from flask_wtf import FlaskForm
from wtforms.fields.core import SelectField

from os import listdir
import json

from app.models.selection import choicesList # ==> ModuleNotFoundError: No module named 'app.models.selection'

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

class SelectForm(FlaskForm):
    choices2 = []
    choices3 = []
    for x in range(0, len(choicesList)):
        if x%2 == 0:
            choices2.append((x, choicesList[x]))
        else:
            choices3.append((x, choicesList[x]))

    brand = SelectField('brand', choices=choices2, validate_choice=False) # ==> ((brand, (productList from brand)), brand#2, (productList from brand#2))
    products = SelectField('product', choices=choices3, validate_choice=False)
    

    
    #(brandsList[0], productList[0]), (brandsList[1], productList[1]), (brandsList[2], productList[2]), (brandsList[3], productList[3]), (brandsList[4], productList[4])