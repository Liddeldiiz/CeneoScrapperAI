from wtforms import Form, StringField, SubmitField, validators
from flask_wtf import FlaskForm

class ProductForm(FlaskForm):
    productID = StringField(
        'Enter product ID',
        [
        validators.DataRequired(message= "Please enter product ID"),
        validators.Length(min=8, max=8, message= "Product ID must have 8 characters"),
        validators.Regexp(regex="^//d+$", message="")
        ])
    submit = SubmitField('Extract', [validators.DataRequired()])