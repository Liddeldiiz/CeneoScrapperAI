from wtforms import StringField, SubmitField, validators
from flask_wtf import FlaskForm

class ProductForm(FlaskForm):
    productID = StringField(
        'Enter product ID',
        [
            validators.DataRequired(message = "Please enter product ID"),
            validators.Length(min=8, max=9, message = "Product ID must have 8 characters"),
            validators.Regexp(regex="^[0-9]+$", message="Product ID can contain only 9 digits")# there are product ID longer then 8 digits, how to change this validator?
        ])
    submit = SubmitField('Extract')