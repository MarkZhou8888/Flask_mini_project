import os
from app import app
##the next line imports functions from flask that we use
#render_template: loads HTML page in templates folder
#request: gets data from form
#redirect: goes to another route
from flask import render_template, request, redirect

from flask_pymongo import PyMongo

# name of database
app.config['MONGO_DBNAME'] = 'test'

#ex
# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:mQvpHemiwKMMXBIt@cluster0-hce3n.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)


# INDEX
#the index route is the home page.
#we have 2 url's that will go to this route '/' and '/index'
@app.route('/')
@app.route('/index')
def index():
    #connect to database
    collection = mongo.db.events
    #query database for all events
    events = list(collection.find({}))
    #check to see if clear all button has been pressed:
    if request.form["clear_all"] == "clear_all":
        for event in events:
            events.delete_one({"event":event["event"]})

    return render_template('index.html', events = events)


# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database
    test = mongo.db.test
    # insert new data
    test.insert({'name': 'last day of school'})
    # return a message to the user
    return "Added data to database!"

@app.route('/input')
def input():
    return render_template('input.html')

# Create a route for ‘/results’ that stores the data from the form
@app.route('/results', methods = ["Get", "Post"])
def results():
    #Get userdata from the form
    userdata = dict(request.form)
    print(userdata)
    # Store the event_name and event_date as separate variables
    event_name = userdata['event_name']
    print(event_name)
    event_date = userdata['event_date']
    print(event_date)
    # Connect to your Mongo cluster and collection and a database called events.
    events = mongo.db.events
    # Insert the name and date of the event to your Mongo events database as a dictionary {“name”: event_name, “date”: event_date}
    events.insert({"name": event_name, "date": event_date})
    #The redirect function is imported on line 3. After reaching the end of the results function, the goal is to run the entire index function.
    return redirect('/index')
