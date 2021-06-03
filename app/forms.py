from numpy import array
from wtforms import StringField, SubmitField, validators
from flask_wtf import FlaskForm
from wtforms.fields.core import SelectField

from os import listdir


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
    brandList = [x.split(".")[0] for x in listdir("app/opinions")]
    productsListPrint = []
    n=0
    for product in brandList:
        productsListPrint += (brandList[n], [x.split(".")[0] for x in listdir("app/opinions/{}".format(product))])
        n+=1

    brand = SelectField('brand', choices=[(product, product[product+1]) for product in productsListPrint if type(product)!=list])
    product = SelectField('product', choices=[])
    