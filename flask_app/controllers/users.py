from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register", methods = ['POST'])
def create_user():
    if user.User.create_user(request.form):
        return redirect('/sightings/home')
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    if user.login_user(request.form):
        return redirect('/sightings/home')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')