from flask_app import app
from flask import flash
import re
from flask_app.config.mysqlconnection import connectToMySQL

db = 'class_project_db'

class Team:
    def __init__(self, data):
        self.id = data['id']
        self.team_name = data['team_name']
        self.player1 = data['player1']
        self.player2 = data['player2']
        self.player3 = data['player3']
        self.player4 = data['player4']
        self.player5 = data['player5']
        self.player6 = data['player6']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add(cls, data):
        query = "INSERT into teams (team_name, player1, player2, player3, player4, player5, player6, user_id) VALUES (%(team_name)s, %(player1)s, %(player2)s, %(player3)s, %(player4)s, %(player5)s, %(player6)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM teams WHERE user_id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM teams;"
        results = connectToMySQL(db).query_db(query)
        teams = []
        for user in results:
            teams.append(cls(user))
        return teams