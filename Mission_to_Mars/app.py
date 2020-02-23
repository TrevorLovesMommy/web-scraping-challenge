from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import pymongo
from flask_pymongo import PyMongo
import scrape_mars
import pandas as pd

#create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# #run scrape function.  this calls the scrape function in scrape_mars.py
# mars_scraped = scrape_mars.scrape()
# print(mars_scraped)

# # Update the Mongo database using update and upsert=True
# mongo.db.collection.update({}, mars_scraped, upsert=True) 



@app.route("/")
def index():
    #get document from mongodb
    mars_data = mongo.db.collection.find_one()

    # print(mars_data)
    # Return the template and mars_data from
    return render_template("index.html", dict=mars_data)
  

# @app.route("/scrape")
# def scraper():
#     mars_data_collection = mongo.db.mars_data_collection
#     mars_scraped = scrape_mars.scrape()
#     mars_data_collection.update({}, mars_scraped, upsert=True)
#     return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

