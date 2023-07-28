from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = 'Propose_help'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owners = []

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM user;'
        results = connectToMySQL(cls.db).query_db(query)
        user = []
        for row in results:
            user.append(cls(row))
        return user

    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM user WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def getEmail(cls, data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        print("results form model:",results)
        if len(results) < 1:
            print("came back false")
            return False
        print("one result")
        return cls(results[0])
    
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO user (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @staticmethod
    def validate(user):
        isValid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            isValid = False
            flash("Email is already in use in our database")
        if len(user['first_name']) < 3:
            isValid = False
            flash("Please use at least 3 characters for the first Name")
        if len(user['last_name']) < 3:
            isValid = False
            flash("Please use at least 3 characters for the last Name")
        if len(user['password']) < 8:
            isValid = False
            flash("Please use least least 8 characters for the password")
        if not EMAIL_REGEX.match(user['email']):
            isValid = False
            flash("Please use proper email format")
        if user['password'] != user['confirm']:
            isValid = False
            flash("Passwords don't match")
        return isValid