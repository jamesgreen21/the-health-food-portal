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

@app.route('/filter_recipes', methods=['POST'])
def filter_recipes():
    if not session.get('logged_in'):
        return render_template('login.html',
                            page="Login")
    else:
        find_filters = request.form.to_dict()

        cuisine_filters=[]
        if 'cuisine' in find_filters:
            cuisine_filters = [find_filters['cuisine']]
        else:
            cuisines=mongo.db.cuisines.find()
            for cuisine in cuisines:
                cuisine_filters.append(cuisine['cuisine_name'])
        
        allergy_filters=[]
        if 'allergies' in find_filters:
            allergy_filters = [find_filters['allergies']]

        return render_template("index.html",
                            page="Home",
                            recipes=mongo.db.master.find({"$and": [
                                {"allergies": {"$nin": allergy_filters}},
                                {"cuisine": {"$in": cuisine_filters}},
                                {"calories": {"$lt": int(find_filters['calories'])+1}},
                                {"cook_time": {"$lt": int(find_filters['cook_time'])+1}},
                                {"protein": {"$lt": int(find_filters['protein'])+1}}
                                ]}),
                            cuisines=mongo.db.cuisines.find(),
                            allergies=mongo.db.allergies.find())


@app.route('/saved_recipes')
def saved_recipes():
    if not session.get('logged_in'):
        return render_template('login.html',
                            page="Login")
    else:
        active_user = session['_id']
        users = mongo.db.users.find({'user_id': active_user})
        user_recipes = ''
        for user in users:
            user_recipes = user["saved_recipes"]

        return render_template("savedrecipes.html",
                            page="Saved Recipes",
                            recipes=mongo.db.master.find({"id": {"$in": user_recipes}}),
                            cuisines=mongo.db.cuisines.find(),
                            allergies=mongo.db.allergies.find())


# https://pythonspot.com/login-authentication-with-flask/
@app.route('/login', methods=['POST'])
def login():
    
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    users = mongo.db.users

    query = users.find({'username': POST_USERNAME, 'password': POST_PASSWORD})
    for result in query:
        session['_id'] = result['user_id']

    if query.count() != 0:
        session['logged_in'] = True
    else:
        flash('The username or password entered is incorrect!')
    return index()
    
@app.route('/create_account', methods=['POST'])
def create_account():
    users = mongo.db.users

    # Set up user
    user_id = users.find_one(sort=[("user_id", 1)])["user_id"]
    new_user = request.form.to_dict()
    new_user['username'] = new_user['username'].lower()
    new_user['first'] = new_user['first'].lower()
    new_user['last'] = new_user['last'].lower()
    new_user.update({'user_id': int(user_id)+1})
    new_user.update({'saved_recipes': []})
    
    # Checks and update or return error
    all_users=users.find()
    for user in all_users:
        if user['username'] == new_user['username']:
            flash('The username you entered already exists!')
            return index()
    
    users.insert_one(new_user)
    
    session['_id'] = new_user['user_id']
    session['logged_in'] = True
    return index()   
    
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


@app.route('/view_recipe')
def view_recipe():
    recipe_id = request.args.get('recipe', None)
    return render_template("viewrecipe.html", 
                            page="View Recipe",
                            cuisines=mongo.db.cuisines.find(),
                            recipe_info=mongo.db.master.find({'id': recipe_id}))
    
@app.route('/save_recipe')
def save_recipe():
    recipe_id = request.args.get('recipe', None)
    active_user = session['_id']
    users = mongo.db.users.find({'user_id': active_user})
    db = mongo.db.users
    for user in users:
        if user['user_id'] == active_user:
            # Check if recipe_id exists
            for v in user["saved_recipes"]:
                if v == recipe_id:
                    user["saved_recipes"].remove(recipe_id)
            user["saved_recipes"].append(recipe_id)
                
            user_id = { "user_id": active_user }
            new_values = { "$set": user }
            db.update_one(user_id, new_values)        

    return render_template("index.html", 
                            page="Home",
                            cuisines=mongo.db.cuisines.find(),
                            recipes=mongo.db.master.find(),
                            allergies=mongo.db.allergies.find())

@app.route('/remove_recipe')
def remove_recipe():
    if not session.get('logged_in'):
        return render_template('login.html',
                            page="Login")
    else:
        recipe_id = request.args.get('recipe', None)
        active_user = session['_id']
        users = mongo.db.users.find({'user_id': active_user})
        db = mongo.db.users
        for user in users:
            if user['user_id'] == active_user:
                user["saved_recipes"].remove(recipe_id)
    
        user_id = { "user_id": active_user }
        new_values = { "$set": user }
        db.update_one(user_id, new_values)        
    
        return saved_recipes()

@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html",
                            cuisines=mongo.db.cuisines.find(),
                            page="Add Recipe")

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.master
    new_recipe = {k.lower():v.lower()
        for k, v in
        request.form.to_dict().items()
    }
    for key in new_recipe:
        if key in ['cook_time','calories','protein']:
            new_recipe[key] = int(new_recipe[key])
            
    recipes.insert_one(new_recipe)
    return redirect(url_for('index'))


@app.route('/update_recipe', methods=['POST'])
def update_recipe():
    recipes = mongo.db.master
    
    updated_rec = {k.lower():v.lower()
        for k, v in
        request.form.to_dict().items()
    }
    for key in updated_rec:
        if key in ['cook_time','calories','protein']:
            updated_rec[key] = int(updated_rec[key])

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