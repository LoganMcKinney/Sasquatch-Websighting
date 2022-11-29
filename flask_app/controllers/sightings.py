from flask import render_template, session, redirect, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask import flash


@app.route("/sightings/home")
def sightings_home():
    if "user_id" not in session:
        flash("You must be logged in to access.")
        return redirect("/")
    
    user = User.get_user_by_id(session["user_id"])
    sightings = Sighting.get_all_sightings()

    return render_template("all_sightings.html", user = user, sightings = sightings)

@app.route("/sighting/<int:sighting_id>")
def sightings_detail(sighting_id):
    user = User.get_user_by_id(session["user_id"])
    sighting = Sighting.get_sighting_by_id(sighting_id)
    return render_template("view_sighting.html", user = user, sighting = sighting)

@app.route("/sighting/create")
def create_new_sighting_page():
    if "user_id" not in session:
        flash("You must be logged in to access.")
        return redirect("/")
    return render_template("new_sighting.html")

@app.route("/sighting/edit/<int:sighting_id>")
def sighting_edit_page(sighting_id):
    if "user_id" not in session:
        flash("You must be logged in to access.")
        return redirect("/")
    sighting = Sighting.get_sighting_by_id(sighting_id)
    return render_template("edit_sighting.html", sighting = sighting)

@app.route("/new_sighting", methods=["POST"])
def create_new_sighting():
    valid_sighting = Sighting.create_sighting(request.form)
    if valid_sighting:
        return redirect('/sightings/home')
    return redirect('/sighting/create')


@app.route("/sighting/<int:sighting_id>", methods=["POST"])
def update_sighting(sighting_id):
    valid_edit = Sighting.update_sighting(request.form, session["user_id"])
    if not valid_edit:
        return redirect(f"/sighting/edit/{sighting_id}")
        
    return redirect("/sightings/home")

@app.route("/sighting/delete/<int:sighting_id>")
def delete_sighting(sighting_id):
    Sighting.delete_sighting(sighting_id)
    return redirect("/sightings/home")