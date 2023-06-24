from flask_app import app
import requests, os
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_app.models.team import Team
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect('/homepage')
    data = {
        "id" : session['user_id']
    }
    players = []
    form_players = request.form.getlist('player')
    for form_player in form_players:
        players.append(form_player)

    datas = {
        'team_name' : request.form['team_name'],
        "player1" : players[0],
        "player2" : players[1],
        "player3" : players[2],
        "player4" : players[3],
        "player5" : players[4],
        "player6" : players[5],
        "user_id" : session['user_id'],
    }

    user = User.get_one(data)
    team = Team.add(datas)
    team_one = Team.get_one(data)
    teams = Team.get_all()

    return render_template('homepage.html',user = user, team = team, teams = teams, team_one = team_one)