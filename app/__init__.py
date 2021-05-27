# from flask package import Flask class
from flask import Flask
# in this line we are defining Flask object
app = Flask(__name__)

# import of routings (routes module) from app package
from app import routes # routes module not importing into this file

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8081)