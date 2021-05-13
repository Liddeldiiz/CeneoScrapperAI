from wtforms import Form, StringField, SubmitField, validators

class ProductForm(Form):
    ProductID = StringField(
        'Enter product ID',
        [
        validators.DataRequired(message= "Please enter product ID"),
        validators.Length(min=8, max=8, message= "Product ID must have 8 characters"),
        validators.Regexp(regex="^//d+$", message="")
        ])
    submit = SubmitField('I accept the TOS', [validators.DataRequired()])