from flask_app import app
import requests, os
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_app.models.team import Team
# from flask_app.models.message import Message
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)
    if not is_valid:
        return redirect('/')
    new_user = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password']),
    }
    id = User.save(new_user)
    if not id:
        flash('Email is already taken!', 'register')
        return redirect('/')
    session['user_id'] = id
    return redirect('/create/team')

@app.route('/login', methods=['POST'])
def login():
    data = {
        "email" : request.form['email']
    }
    user = User.get_user_by_email(data)

    if not user:
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/homepage')

@app.route('/homepage')
def homepage():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }

    user = User.get_one(data)
    users = User.get_all()
    team = Team.add(data)
    team_one = Team.get_one(data)
    teams = Team.get_all()
    pick = False
    # messages = Message.get_all()
    # sender = User.get_sender(data)
    return render_template('homepage.html', user = user, users = users, teams = teams, team = team, team_one = team_one, pick = pick)

@app.route('/edit/profile/<int:id>')
def edit_profile(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    return render_template("edit_profile.html",user=User.get_one(data))

@app.route('/update/profile/<int:id>', methods=['POST'])
def update_profile(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not User.validate_update(request.form):
        return redirect(f'/edit/profile/{id}')
    data = {
        "id": id,
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
    }
    User.update(data)
    return redirect('/homepage')

@app.route('/leaderboard')
def leaderboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    return render_template("leaderboard.html", user=User.get_one(data))

@app.route('/tournament/leaderboard')
def tournament_leaderboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }

    url = "https://live-golf-data.p.rapidapi.com/leaderboard"
    querystring = {"tournId":"012","year":"2022"}
    headers = {
        "X-RapidAPI-Host": "live-golf-data.p.rapidapi.com",
        # "X-RapidAPI-Key": "" Removed to prevent unauthorized API calls
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    session['cutline'] = response.json()['cutLines'][0]['cutScore']
    places = []
    session['places'] = places
    fnames = []
    session['fnames'] = fnames
    lnames = []
    session['lnames'] = lnames
    scores = []
    session['scores'] = scores
    rones = []
    session['rones'] = rones
    rtwos = []
    session['rtwos'] = rtwos
    rthrees = []
    session['rthrees'] = rthrees
    rfours = []
    session['rfours'] = rfours

    for x in range(70):
        places.append((response.json()['leaderboardRows'][x]['position']))
        fnames.append((response.json()['leaderboardRows'][x]['firstName']))
        lnames.append((response.json()['leaderboardRows'][x]['lastName']))
        scores.append((response.json()['leaderboardRows'][x]['total']))
        rones.append((response.json()['leaderboardRows'][x]['rounds'][0]['scoreToPar']))
        rtwos.append((response.json()['leaderboardRows'][x]['rounds'][1]['scoreToPar']))
        rthrees.append((response.json()['leaderboardRows'][x]['rounds'][2]['scoreToPar']))
        rfours.append((response.json()['leaderboardRows'][x]['rounds'][3]['scoreToPar']))


    return render_template('tournament_leaderboard.html', user=User.get_one(data))

@app.route('/create/team')
def create_team():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }

    url = "https://live-golf-data.p.rapidapi.com/leaderboard"
    querystring = {"tournId":"012","year":"2022"}
    headers = {
        "X-RapidAPI-Host": "live-golf-data.p.rapidapi.com",
        # "X-RapidAPI-Key": "" Removed to prevent unauthorized API calls
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    places = []
    session['places'] = places
    fnames = []
    session['fnames'] = fnames
    lnames = []
    session['lnames'] = lnames
    scores = []
    session['scores'] = scores

    for x in range(70):
        places.append((response.json()['leaderboardRows'][x]['position']))
        fnames.append((response.json()['leaderboardRows'][x]['firstName']))
        lnames.append((response.json()['leaderboardRows'][x]['lastName']))
        scores.append(str(response.json()['leaderboardRows'][x]['total']))

    return render_template('create_team.html', user=User.get_one(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')