import os
from flask import Flask, jsonify, render_template, json
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'healthyFoodDB'
app.config["MONGO_URI"] = 'mongodb+srv://root:Meagain00@healthyfoodportal-2dtl3.mongodb.net/healthyFoodDB?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def index():
	comment_dict = {
	       'recipe_name' : 'Test',
	       'recipe_description' : 'Test description',
	       'calories' : 350}    
	return render_template("test.html",data=comment_dict)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)