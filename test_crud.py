import pymongo
import os

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "healthyFoodDB"
COLLECTION_NAME = "master"

def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e

def show_menu():
    print("")
    print("1. Add a record")
    print("2. Find a record by name")
    print("3. Edit a record")
    print("4. Delete a record")
    print("5. Exit")
    option = input("Enter option: ")
    return option

def get_record():
    print("")
    recipe_name = input("Enter Recipe Name > ")
    try:
        doc = coll.find_one({'recipe_name': recipe_name.lower()})
    except:
        print("Error accessing the db")
    if not doc:
        print("")
        print("Error! No results found.")
    return doc

def add_record():
    print("")
    recipe_name = input("Enter Recipe Name > ")
    recipe_description = input("Enter Recipe Description > ")
    cooking_instructions = input("Enter Cooking Instructions > ")
    prep_time = input("Enter Prep Time > ")
    cook_time = input("Enter Cook Time > ")
    protein = input("Enter Protein > ")
    calories = input("Enter Calories > ")
    cuisine = input("Enter Cuisine > ")
    photo_id = input("Enter Photo ID > ")
    
    new_doc = {'recipe_name': recipe_name.lower(),'recipe_description':
                recipe_description.lower(),'cooking_instructions':
                cooking_instructions.lower(),'prep_time':prep_time.lower(),
                'cook_time':cook_time.lower(),'protein':protein.lower(),
                'calories':calories.lower(),'cuisine':cuisine.lower(),
                'photo_id':photo_id.lower()}
    try:
        coll.insert(new_doc)
        print("")
        print("Document inserted")
    except:
        print("Error accessing the db")

def find_record():
    doc = get_record()
    if doc:
        print("")
        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())

def edit_record():
    doc = get_record()
    if doc:
        update_doc = {}
        print("")
        for k, v in doc.items():
            if k != "_id":
                update_doc[k] = input(k.capitalize() + " [" + v + "] > ")
                if update_doc[k] == "":
                    update_doc[k] = v
        try:
            coll.update_one(doc, {'$set': update_doc})
            print("")
            print("Document updated")
        except:
            print("Error accessing the db")

def delete_record():
    doc = get_record()
    if doc:
        print("")
        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())
        print("")
        confirmation = input(
            "Are you sure you want to delete this record?\nY or N >")
        print("")
        if confirmation.lower() == 'y':
            try:
                coll.remove(doc)
                print("Document deleted!")
            except:
                print("Error accessing the db")
        else:
            print("Document not deleted")
            
def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            delete_record()
        elif option == "5":
            conn.close()
            break
        else:
            print("Invalid option")
        print("")

conn = mongo_connect(MONGODB_URI)
coll = conn[DBS_NAME][COLLECTION_NAME]

main_loop()