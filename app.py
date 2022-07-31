
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
# connect to mongo db and collection
db = client.mars_db
collection = db.info

@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    information = collection.find()[0]
    return render_template("index.html", information=information)

@app.route('/scrape')
def scrape():
    data = scrape_mars.scrape()
    collection.update(
        {},
        data,
        upsert=True
    )
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)