from flask import (Flask, render_template, redirect, request, url_for, request,
                   jsonify, json, flash, session, abort)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'healthyFoodDB'
app.config["MONGO_URI"] = "mongodb+srv://root:Meagain00@healthyfoodportal-2d" \
                          "tl3.mongodb.net/healthyFoodDB?retryWrites=true&w=" \
                          "majority"

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    """
    Home Page - All recipes
    """
    if not session.get('logged_in'):
        return render_template('login.html', page="Login")
    else:
        active_user = session['_id']
        user_detail = get_user_detail(active_user)
        username = user_detail["user_name"]
        user_recipes = user_detail["user_saved_recipes"]
        return render_template("index.html",
                               page="Home",
                               username=username,
                               user=active_user,
                               recipes=mongo.db.master.find(),
                               saved_recipes=user_recipes,
                               cuisines=mongo.db.cuisines.find(),
                               allergies=mongo.db.allergies.find())


@app.route('/login', methods=['POST'])
def login():
    """
    Login - https://pythonspot.com/login-authentication-with-flask/
    """
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    users = mongo.db.users
    user_check = users.find(
        {'username': POST_USERNAME, 'password': POST_PASSWORD})
    if user_check.count() != 0:
        session['logged_in'] = True
        for result in user_check:
            session['_id'] = result['user_id']
    else:
        flash('The username or password entered is incorrect!')
    return index()


@app.route("/logout")
def logout():
    """
    Login - https://pythonspot.com/login-authentication-with-flask/
    """
    session['logged_in'] = False
    return index()


@app.route('/create_account', methods=['POST'])
def create_account():
    """
    Login - Create User
    """
    users = mongo.db.users

    # Set up user
    user_id = users.find_one(sort=[("user_id", -1)])["user_id"]
    new_user = request.form.to_dict()
    new_user['username'] = new_user['username'].lower()
    new_user['first'] = new_user['first'].lower()
    new_user['last'] = new_user['last'].lower()
    new_user.update({'user_id': int(user_id)+1})
    new_user.update({'saved_recipes': []})

    # Checks and update or return error
    all_users = users.find()
    for user in all_users:
        if user['username'] == new_user['username']:
            flash('The username you entered already exists!')
            return index()

    users.insert_one(new_user)

    session['_id'] = new_user['user_id']
    session['logged_in'] = True
    return index()


@app.route('/filter_recipes', methods=['POST'])
def filter_recipes():
    """
    Search Nav Filter
    """
    if not session.get('logged_in'):
        return render_template('login.html', page="Login")
    else:
        active_user = session['_id']
        user_detail = get_user_detail(active_user)
        username = user_detail["user_name"]
        user_recipes = user_detail["user_saved_recipes"]
        
        active_filters = request.form.to_dict()
        cuisine_filters = []
        allergy_filters = []
        calories_filter = {"calories": {"$lt": int(active_filters['calories'])+1}}
        time_filter = {"cook_time": {"$lt": int(active_filters['cook_time'])+1}}
        protein_filter = {"protein": {"$lt": int(active_filters['protein'])+1}}
        
        if 'cuisine' in active_filters:
            cuisine_filters = {"cuisine": {"$in": [active_filters['cuisine']]}}
        else:
            cuisine_filters = {"cuisine": {"$nin": [""]}}

        if 'allergies' in active_filters:
            allergy_filters = {"allergies": {"$nin": [active_filters['allergies']]}}
        else:
            allergy_filters = {"allergies": {"$nin": [""]}}

        return render_template("index.html", 
                               page="Home",
                               username=username,
                               user=active_user,
                               saved_recipes=user_recipes,
                               cuisines=mongo.db.cuisines.find(),
                               allergies=mongo.db.allergies.find(),
                               recipes=mongo.db.master.find({"$and": [
                               allergy_filters,
                               cuisine_filters,
                               calories_filter,
                               time_filter,
                               protein_filter]}))


@app.route('/view_recipe')
def view_recipe():
    """
    View Recipe
    """
    recipe_id = request.args.get('recipe', None)

    if not session.get('logged_in'):
        return render_template('login.html', page="Login")
    else:
        active_user = session['_id']
        user_detail = get_user_detail(active_user)
        username = user_detail["user_name"]
        user_recipes = user_detail["user_edit_recipes"]
        print(user_recipes)
        edit_mode = True if int(recipe_id) in user_recipes else False

        return render_template("viewrecipe.html",
                               page="View Recipe",
                               username=username,
                               cuisines=mongo.db.cuisines.find(),
                               form_cuisines=mongo.db.cuisines.find(),
                               recipe_info=mongo.db.master.find(
                                   {'id': int(recipe_id)}),
                               allergies=mongo.db.allergies.find(),
                               view_allergies=mongo.db.allergies.find(),
                               select_allergies=mongo.db.allergies.find(),
                               form_allergies=mongo.db.allergies.find(),
                               edit_mode=edit_mode)


@app.route('/save_recipe')
def save_recipe():
    """
    User - Add to Saved Recipe
    """
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
            user_id = {"user_id": active_user}
            new_values = {"$set": user}
            users_db.update_one(user_id, new_values)

    return index()


@app.route('/remove_recipe')
def remove_recipe():
    """
    User - Remove from Saved Recipe
    """
    if not session.get('logged_in'):
        return render_template('login.html', page="Login")
    else:
        recipe_id = request.args.get('recipe', None)
        active_user = session['_id']
        users = mongo.db.users.find({'user_id': active_user})
        db = mongo.db.users
        for user in users:
            if user['user_id'] == active_user:
                user["saved_recipes"].remove(int(recipe_id))

        user_id = {"user_id": active_user}
        new_values = {"$set": user}
        db.update_one(user_id, new_values)
        return saved_recipes()


@app.route('/saved_recipes')
def saved_recipes():
    """
    Saved Recipes Page
    """
    if not session.get('logged_in'):
        return render_template('login.html', page="Login")
    else:
        active_user = session['_id']
        users = mongo.db.users.find({'user_id': active_user})
        user_recipes = ''
        username = ''
        for user in users:
            user_recipes = list(map(int, user["saved_recipes"]))
            username = user["first"] + " " + user["last"]

        return render_template("savedrecipes.html",
                               page="Saved Recipes",
                               username=username,
                               recipes=mongo.db.master.find(
                                   {"id": {"$in": user_recipes}}),
                               cuisines=mongo.db.cuisines.find(),
                               allergies=mongo.db.allergies.find())


@app.route('/edit_recipes', methods=['POST', 'GET'])
def edit_recipes():
    """
    Home Page - Editable recipes filter
    """
    if not session.get('logged_in'):
        return render_template('login.html', page="Login")
    else:
        active_user = session['_id']
        user_detail = get_user_detail(active_user)
        username = user_detail["user_name"]
        user_editable_recipes = user_detail["user_edit_recipes"]
        recipes=mongo.db.master.find({"user_id": {"$in": [active_user]}})
        
        return render_template("index.html",
                               page="Home",
                               username=username,
                               user=active_user,
                               recipes=recipes,
                               saved_recipes=user_editable_recipes,
                               cuisines=mongo.db.cuisines.find(),
                               allergies=mongo.db.allergies.find())
    

@app.route('/add_recipe')
def add_recipe():
    """
    Add Recipes Page
    """
    if not session.get('logged_in'):
        return render_template('login.html', page="Login")
    else:
        active_user = session['_id']
        users = mongo.db.users.find({'user_id': active_user})
        user_recipes = ''
        username = ''
        for user in users:
            user_recipes = list(map(int, user["saved_recipes"]))
            username = user["first"] + " " + user["last"]

        return render_template("addrecipe.html",
                               cuisines=mongo.db.cuisines.find(),
                               form_cuisines=mongo.db.cuisines.find(),
                               page="Add Recipe",
                               username=username,
                               allergies=mongo.db.allergies.find(),
                               form_allergies=mongo.db.allergies.find(),
                               select_allergies=mongo.db.allergies.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    """
    Insert recipe to MongoDB master collection
    """
    active_user = session['_id']
    recipes = mongo.db.master
    allergies_cur = mongo.db.allergies.find()
    allergy_names = request.form.getlist('allergies')
    allergy_urls = []
    new_recipe = request.form.to_dict()
    # Update allergies
    for allergies in allergies_cur:
        if allergies['allergy_name'] in allergy_names:
            allergy_urls.append(allergies['image_id'])

    # Update number values
    for key in new_recipe:
        if key in ['cook_time', 'calories', 'protein']:
            new_recipe[key] = int(new_recipe[key])

    # Update id
    recipe_id = recipes.find_one(sort=[("id", -1)])["id"]
    new_recipe.update({'id': recipe_id+1})
    new_recipe.update(
        {'allergies': allergy_names, 'allergy_url': allergy_urls})
    new_recipe.update({'user_id': active_user})

    recipes.insert_one(new_recipe)
    return redirect(url_for('index'))


@app.route('/update_recipe', methods=['POST'])
def update_recipe():
    """
    Update recipe in MongoDB master collection
    """
    recipes = mongo.db.master
    allergies_cur = mongo.db.allergies.find()
    allergy_names = request.form.getlist('allergies')
    allergy_urls = []

    # Update allergies
    for allergies in allergies_cur:
        if allergies['allergy_name'] in allergy_names:
            allergy_urls.append(allergies['image_id'])

    updated_rec = request.form.to_dict()
    for key in updated_rec:
        if key in ['cook_time', 'calories', 'protein']:
            updated_rec[key] = int(updated_rec[key])

    recipe_id = {"id": int(updated_rec["id"])}
    updated_rec.pop("id")
    updated_rec.update(
        {'allergies': allergy_names, 'allergy_url': allergy_urls})

    new_values = {"$set": updated_rec}
    print(recipe_id, new_values)
    recipes.update_one(recipe_id, new_values)
    return redirect(url_for('index'))


# Helper functions
def get_user_detail(active_user):
    """
    Return dict of user details
    """
    users = mongo.db.users.find({'user_id': active_user})
    recipes = mongo.db.master.find()
    editable_recipes = []
    for recipe in recipes:
        if active_user == recipe['user_id']:
            editable_recipes.append(recipe['id'])
    for user in users:
        return {
            "user_name": user["first"] + " " + user["last"], 
            "user_saved_recipes": list(map(int, user["saved_recipes"])),
            "user_edit_recipes":  editable_recipes
        }


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
