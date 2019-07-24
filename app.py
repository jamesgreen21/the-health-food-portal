import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'healthyFoodDB'
app.config["MONGO_URI"] = 'mongodb+srv://root:Meagain00@healthyfoodportal-2dtl3.mongodb.net/healthyFoodDB?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    myrecipes = dumps(mongo.db.master.find())
    return render_template("recipes.html", 
                            recipes=jsonify(myrecipes), 
                            page="Home")
   
@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html",
                            cuisines=mongo.db.cuisines.find(),
                            page="Add Recipe")

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.master
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)