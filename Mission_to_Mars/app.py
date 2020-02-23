from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars

app = Flask(__name__)




#mongo database = mars_db
#mongo table = mars_data_collection
#mongo document = mars_data


# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
db.mars_data_collection.drop()

# Creates a collection in the database and inserts document from scrape_mars.py
db.mars_data_collection.insert_one(
        {
            'player': 'Jessica',
            'position': 'Point Guard'
        }
)


# #Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
# mongo = PyMongo(app)


# @app.route("/")
# def index():
#     #stores scraped mars data in a list
#     mars_data = mongo.db.mars_data_collection.find())
#     print(mars_data)
#     # Return the template with the teams mars_data list passed in
#     return render_template("index.html", dict=mars_data)

# @app.route("/scrape")
# def scraper():
#     mars_data_collection = mongo.db.mars_data_collection
#     mars_scraped = scrape_mars.scrape()
#     mars_data_collection.update({}, mars_scraped, upsert=True)
#     return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

