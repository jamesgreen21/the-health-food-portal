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
    '''Home Page - All recipes'''
    if not session.get('logged_in'):
        return render_template('login.html',
                            page="Login")
    else:
        active_user = session['_id']
        users = mongo.db.users.find({'user_id': active_user})
        user_recipes = ''
        for user in users:
            user_recipes = list(map(int, user["saved_recipes"]))

        recipes_cur=mongo.db.master.find()
        allergies_cur=mongo.db.allergies.find()
        allergies_dict = {}
        for allergy in allergies_cur:
            allergies_dict.update({allergy["allergy_name"]: allergy["image_id"]})
            
        print(allergies_dict)

        for recipes in recipes_cur:
            allergy_urls = []
            
            if 'allergies' in recipes:
                for recipe_allergy in recipes['allergies']:
                    for allergy in allergies_dict:
                        if recipe_allergy == allergy:
                            allergy_urls.append(allergies_dict[allergy])
                            break
                recipes['allergies'] = allergy_urls
                allergy_urls.clear()
        
        print(recipes)
        #     for allergy in allergies:
        #         if k == allergy:
        #             print(v)
            #     for i in range(len(recipe["allergies"])):
            #         
            #             if recipe["allergies"][i] == allergy["allergy_name"]:
            #                 allergy_img =+  allergy["image_id"]
        
        # recipes["allergies"] = allergy_img

        return render_template("index.html",
                            page="Home",
                            # recipes=recipes,
                            saved_recipes=user_recipes,
                            cuisines=mongo.db.cuisines.find(),
                            allergies=mongo.db.allergies.find())

@app.route('/filter_recipes', methods=['POST'])
def filter_recipes():
    '''Home Page - Filter'''
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
        else:
            allergies=mongo.db.allergies.find()
            for allergy in allergies:
                allergy_filters.append(allergy['allergy_name'])

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

@app.route('/login', methods=['POST'])
def login():
    '''Login - https://pythonspot.com/login-authentication-with-flask/'''
    
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    users = mongo.db.users

    user_check = users.find({'username': POST_USERNAME, 'password': POST_PASSWORD})
    if user_check.count() != 0:
        session['logged_in'] = True
        for result in user_check:
            session['_id'] = result['user_id']
    else:
        flash('The username or password entered is incorrect!')
    return index()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@app.route('/create_account', methods=['POST'])
def create_account():
    '''Login - Create User'''
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
    
@app.route('/view_recipe')
def view_recipe():
    '''View Recipe'''
    recipe_id = request.args.get('recipe', None)
    
    if not session.get('logged_in'):
        return render_template('login.html',
                            page="Login")
    else:
        active_user = session['_id']
        users = mongo.db.users.find({'user_id': active_user})
        user_recipes = ''
        for user in users:
            user_recipes = list(map(int, user["saved_recipes"]))

        edit_mode = False
        if int(recipe_id) in user_recipes:
            edit_mode = True

        return render_template("viewrecipe.html", 
                                page="View Recipe",
                                cuisines=mongo.db.cuisines.find(),
                                form_cuisines=mongo.db.cuisines.find(),
                                recipe_info=mongo.db.master.find({'id': int(recipe_id)}),
                                allergies=mongo.db.allergies.find(),
                                view_allergies=mongo.db.allergies.find(),
                                select_allergies=mongo.db.allergies.find(),
                                form_allergies=mongo.db.allergies.find(),
                                edit_mode=edit_mode)

@app.route('/save_recipe')
def save_recipe():
    ''' User - Save recipe'''
    recipe_id = request.args.get('recipe', None)
    active_user = session['_id']
    users = mongo.db.users.find({'user_id': active_user})
    users_db = mongo.db.users
    for user in users:
        if user['user_id'] == active_user:
            # Check if recipe_id exists
            for v in user["saved_recipes"]:
                if v == int(recipe_id):
                    user["saved_recipes"].remove(int(recipe_id))
            user["saved_recipes"].append(int(recipe_id))
            user.pop('_id')
                
            user_id = { "user_id": active_user }
            new_values = { "$set": user }
            users_db.update_one(user_id, new_values)

    return index()
    
@app.route('/remove_recipe')
def remove_recipe():
    '''User - Remove recipe'''
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
                user["saved_recipes"].remove(int(recipe_id))
    
        user_id = { "user_id": active_user }
        new_values = { "$set": user }
        db.update_one(user_id, new_values)        
    
        return saved_recipes()

@app.route('/saved_recipes')
def saved_recipes():
    '''User - Manage Recipes'''
    if not session.get('logged_in'):
        return render_template('login.html',
                            page="Login")
    else:
        active_user = session['_id']
        users = mongo.db.users.find({'user_id': active_user})
        user_recipes = ''
        for user in users:
            user_recipes = list(map(int, user["saved_recipes"]))
            
        return render_template("savedrecipes.html",
                            page="Saved Recipes",
                            recipes=mongo.db.master.find({"id": {"$in": user_recipes}}),
                            cuisines=mongo.db.cuisines.find(),
                            allergies=mongo.db.allergies.find())

# Add Recipe
@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html",
                            cuisines=mongo.db.cuisines.find(),
                            form_cuisines=mongo.db.cuisines.find(),
                            page="Add Recipe",
                            allergies=mongo.db.allergies.find(),
                            form_allergies=mongo.db.allergies.find(),
                            select_allergies=mongo.db.allergies.find())

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    '''Insert recipe to db'''
    recipes = mongo.db.master
    allergy_select = request.form.getlist('allergies')
    new_recipe = request.form.to_dict()
    
    for key in new_recipe:
        if key in ['cook_time','calories','protein']:
            new_recipe[key] = int(new_recipe[key])
            
    # # Update id
    recipe_id = recipes.find_one(sort=[("id", -1)])["id"]
    new_recipe.update({'id': recipe_id+1})
    new_recipe.update({'allergies': allergy_select})
    
    recipes.insert_one(new_recipe)
    return redirect(url_for('index'))

@app.route('/update_recipe', methods=['POST'])
def update_recipe():
    '''Update recipe on db'''
    recipes = mongo.db.master
    allergy_select = request.form.getlist('allergies')
    
    updated_rec = request.form.to_dict()
    for key in updated_rec:
        if key in ['cook_time','calories','protein']:
            updated_rec[key] = int(updated_rec[key])
    
    recipe_id = { "id": int(updated_rec["id"]) }
    updated_rec.pop("id")
    updated_rec.update({'allergies': allergy_select})

    new_values = { "$set": updated_rec }
    print(recipe_id, new_values)
    recipes.update_one(recipe_id, new_values)
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)