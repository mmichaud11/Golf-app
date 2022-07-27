from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.config.mysqlconnection import connectToMySQL
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'class_project_db'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT into users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_sender(cls, data):
        query = "SELECT * FROM users JOIN messages ON messages.id = users.id WHERE messages.id = %(id)s"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,user)
        if len(user['first_name']) < 2:
            is_valid = False
            flash('First name must be at least 2 characters', 'register')
        if len(user['last_name']) < 2:
            is_valid = False
            flash('Last name must be at least 2 characters', 'register')
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash('Email not valid', 'register')
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if len(user['password']) < 8:
            is_valid = False
            flash('Password must be at least 2 characters', 'register')
        if user['password'] != user['confirm_password']:
            is_valid = False
            flash("Passwords do not match!", "register")
        return is_valid

    @staticmethod
    def validate_update(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,user)
        if len(user['first_name']) < 2:
            is_valid = False
            flash('First name must be at least 2 characters', 'update')
        if len(user['last_name']) < 2:
            is_valid = False
            flash('Last name must be at least 2 characters', 'update')
        return is_valid