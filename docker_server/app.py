from flask import Flask, render_template, request
import subprocess as sp
from pymongo import MongoClient
from mongopass import mongopass

app = Flask(__name__)


client = MongoClient("mongodb+srv://admin:<password>@cluster0.rsbrxww.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.test

myCollection = db.cluster0

@app.route("/")
def my_home():
    date = sp.getoutput("date /t")
    return render_template("home.html", date = date)

@app.route("/curd")
def insert_val():
    return render_template("curd.html")

@app.route("/read")
def read():
    cursor = myCollection.find()
    for record in cursor:
        name = record['name']
        print(record)
    return render_template("res.html", res=name)

@app.route("/insert")
def insert():
    name = request.args.get("name")
    address = request.args.get("address")
    val = { "name": name, "address": address }
    x = myCollection.insert_one(val)
    return render_template("res.html", res=x)

@app.route("/delete")
def delete():
    name = request.args.get("name")
    myQuery = { "name": name }
    myCollection.delete_one(myQuery)
    x = "Record delete"
    return render_template("res.html", res=x)

@app.route("/update")
def update():
    name = request.args.get("name")
    new_address = request.args.get("new_address")
    query = { "name": name }
    val = { "$set": { "address": new_address } }
    myCollection.update_one(query, val)
    x = "Record Updated"
    return render_template("res.html", res=x)

if __name__ == "__main__":
    app.run(debug=True, host='')