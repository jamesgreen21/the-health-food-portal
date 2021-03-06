# The Healthy Food Portal

This is an app where users can log into or create a simple account to gain access to various recipes, which they can save to review later, and can create brand new recipes, which they can later edit if required. The app gives the user the ability to filter the recipes by cuisines, removing allergies, setting maximum cooking time and calories.

Website link: INPUT

## UX
 
The apps focus is to give the user a hassel free environment where they can view, store and create recipes that are more on the healthy side. The app has a simple layout with a small number of settings atributed to each recipe:

-	Recipe Name
-   Description
-   Photo URL - this is used to display the photo through the use of a URL link rather than an uploaded picture
-   Cooking Instructions
-   Prep/Cook Time
-   Calories
-   Protein
-   Allergies (if any)
  
The app gives the user a helpful display for each recipe available, highlighting the key factors within each recipe (e.g. allergies), and allowing the user to view further detail if required.

All buttons and links are consistent along with the color scheme and layouts to maximise UX. Each page load includes animated effects to give the user a smoother transitioning.

New user creations are greeted by helper pop-ups that load up on the Home page for the first time a user logs in.

### Display

The website is mobile-first responsive design, making use of the Bootstrap grid system to ensure all functionality contained in the app is availble to the user to interact with, whatever their display configurations. 

## Features

There are a number of features throughout the app ranging from search functionality to user help pop-ups
 
### Current Features

- Login Page
    - Login: Allows existing users to login so that all of their relevant information is available to them
    - Create User: Allows new or existing users to create a new account for the app, provided they use credentials that haven't already been used.
- Home Page
    - View Recipe: Indepth view of the recipe
    - Save Recipe: Allows users to save recipes to review later within the Saved Recipes page. These can later be removed by using the Saved Recipes Page, Remove Recipe button
    - Conditional formatting: Used in the calories section to assist with User choice, highlighting those with high calories in red and low in green
- Search: A filtering tool, which affects the display on the Home page
    - Cuisine: Allows the user to choose from the list of set Cuisines available on the app
    - Allergies: Allows the user to filter out any known allergies they wish to remove
    - Cooking Time: Gives the user the ability to scale down time spent on prep and cook
    - Calories: Allows the user to reduce the total recipe calories for those that desire a healthier option
- Manage Recipes
    - Add Recipe: Give the users the ability to add completely new recipes, in the format of a form, the details of which are covered below
    - Edit Recipe: Applies a filter to the Home page that shows only the recipes that are editable by the user logged in. This is in accordance with the user whom created the recipe
- Saved Recipes
    - View Recipe: Indepth view of the recipe
    - Remove Recipe: Allows users to remove recipes from within their Saved Recipes page. These can later be added back using the Home Page, Save Recipe button
    - Conditional formatting: Used in the calories section to assist with User choice, highlighting those with high calories in red and low in green
-Logout: Allows users to completely log out of the app

### Features Left to Implement

- Additional Recipe attributes
- An admin page for handling the app data structures better, e.g. managing the Cuisines and Allergies available and the ability to amend/delete users

## Getting Started

Instructions

### Installing

The following installations are required to run the app locally:

---
astroid==1.6.6
awscli==1.16.189
botocore==1.12.179
colorama==0.3.9
Django==2.0.2
dnspython==1.16.0
docutils==0.14
Flask==1.1.1
Flask-PyMongo==2.3.0
ikp3db==1.1.4
isort==4.3.21
itsdangerous==1.1.0
jedi==0.11.1
Jinja2==2.10.1
jmespath==0.9.4
lazy-object-proxy==1.4.1
mccabe==0.6.1
parso==0.1.1
pbr==5.3.1
pyasn1==0.4.5
pylint==1.8.1
pylint-django==0.8.0
pylint-flask==0.5
pylint-plugin-utils==0.5
pymongo==3.8.0
python-dateutil==2.8.0
pytz==2019.1
PyYAML==5.1
rsa==3.4.2
s3transfer==0.2.1
six==1.12.0
stevedore==1.30.1
urllib3==1.25.3
virtualenv==16.2.0
virtualenv-clone==0.5.3
virtualenvwrapper==4.8.4
Werkzeug==0.15.5
wrapt==1.11.2
---

### Compatibility

The following browsers are compatible with the app:

- Google Chome
- Firefox

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

The website has undergone testing on all features:

### And coding style tests

Explain what these tests test and why

```
Give an example
```

### Bugs

There are currently two bugs that appear in the console once the website has been generated. The TypeError refers to a .length command that returns the count of records within the data set, and is used in a For loop. The count and loop both work having tested it through the console log, however, I have been unable to determine the reason for the bug.

 - Uncaught (in promise) TypeError: Cannot read property 'length' of undefined
    at getMapLocations (scheduler.js:666)
    at initMap (scheduler.js:514)
    at js?key=AIzaSyCsI1fq6JVdHRu4UgMmIuZXCTO0UPzF8JQ&callback=initMap:123
    at js?key=AIzaSyCsI1fq6JVdHRu4UgMmIuZXCTO0UPzF8JQ&callback=initMap:123
    
 - GET https://mbsync-tardis-tech-scheduler-jamesgreen21.c9users.io/favicon.ico 404 (Not Found)

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Bootstrap](https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css) - The web framework used
* [Font Awesome](https://fonts.googleapis.com/css?family=Lato|Roboto&display=swap) - Web icon library
* [jQuery](https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js) - Used to handle JS functions
* [flask](http://flask.palletsprojects.com/en/1.1.x/) - The backend framework used
* [flask_pymongo](https://api.mongodb.com/python/current/) - The database query language used
* [mongoDB](https://www.mongodb.com/) - The database used

## Acknowledgments

* Python Tutorials (https://pythonspot.com/login-authentication-with-flask/) - code used for user handling such as login