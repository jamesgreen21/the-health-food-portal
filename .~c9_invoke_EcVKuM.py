import os
from flask import Flask, render_template, redirect, request, url_for, request, jsonify, json, flash, session, abort
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'healthyFoodDB'
app.config["MONGO_URI"] = 'mongodb+srv://root:Meagain00@healthyfoodportal-2dtl3.mongodb.net/healthyFoodDB?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')
def index():
    if not session.get('logged_in'):
        return render_template('login.html',
                            page="Login")
    else:
        return render_template("index.html",
                            page="Home",
                            recipes=mongo.db.master.find(),
                            cuisines=mongo.db.cuisines.find(),
                            allergies=mongo.db.allergies.find())


# https://pythonspot.com/login-authentication-with-flask/
@app.route('/login', methods=['POST'])
def do_admin_login():
    
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    users = mongo.db.users

    query = users.find({'username': POST_USERNAME, 'password': POST_PASSWORD})
    for result in query:
        session['id'] = result['user_id']

    if query.count() != 0:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return index()
    
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


# @app.route('/get_recipes')
# def get_recipes():
#     # Gets all recipe data as json 
#     try:
#         docs=[]
#         for doc in mongo.db.master.find():
#             doc['_id'] = str(doc['_id'])
#             docs.append(doc)
#         return jsonify(docs)
#     except Exception as e:
#         return str(e)

@app.route('/view_recipe')
def view_recipe():
    recipe_id = request.args.get('recipe', None)
    return render_template("viewrecipe.html", 
                            page="View Recipe",
                            cuisines=mongo.db.cuisines.find(),
                            recipes=mongo.db.master.find(),
                            recipe_info=mongo.db.master.find({'id': recipe_id}))
    
@app.route('/save_recipe')
def save_recipe():
    recipe_id = request.args.get('recipe', None)
    return render_template("index.html", 
                            page="View Recipe",
                            cuisines=mongo.db.cuisines.find(),
                            recipes=mongo.db.master.find(),
                            recipe_info=mongo.db.master.find({'id': recipe_id}))

# @app.route('/save_recipe', methods=['GET, ''POST'])
# def save_recipe():
    # recipe_id = request.args.get('recipe', None)
    # user = mongo.db.users.find({'id': session['id']})
    # print(user['saved_recipes'])
    # return index()

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


@app.route('/update_recipe', methods=['POST'])
def update_recipe():
    recipes = mongo.db.master
    updated_rec = request.form.to_dict()
    recipe_id = { "id": updated_rec["id"] }
    updated_rec.pop("id")
    new_values = { "$set": updated_rec }
    recipes.update_one(recipe_id, new_values)
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)