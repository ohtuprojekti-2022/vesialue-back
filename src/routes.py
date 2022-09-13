from flask import render_template, request, redirect
from app import app
from services.inventory_service import inventory_service


@app.route("/")
def index():
    return "Hello world!"

@app.route("/add_inventory", methods=["POST"])
def add_inventory():
    name = request.form["name"]
    email = request.form["email"]
    phonenumber = request.form["phonenumber"]
    other = request.form["other"]

    succes, error = inventory_service.add_inventory(name, email, phonenumber, other)
    if succes:
        return redirect("/")

    return render_template("index.html", input_error=error)
