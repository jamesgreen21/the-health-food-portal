import os
from flask import Flask, render_template, redirect, request, url_for, request, jsonify, json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'healthyFoodDB'
app.config["MONGO_URI"] = 'mongodb+srv://root:Meagain00@healthyfoodportal-2dtl3.mongodb.net/healthyFoodDB?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                            page="Home",
                            cuisines=mongo.db.cuisines.find(),
                            allergies=mongo.db.allergies.find())


@app.route('/get_recipes')
def get_recipes():
    try:
        docs=[]
        for doc in mongo.db.master.find():
            doc['_id'] = str(doc['_id'])
            docs.append(doc)
        return jsonify(docs)
    except Exception as e:
        return str(e)

@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html",
                            cuisines=mongo.db.cuisines.find(),
                            page="Add Recipe")

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.master
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)