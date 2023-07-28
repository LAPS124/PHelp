from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

db = 'Propose_help'


class Job:

    db = 'Propose_help'

    def __init__ (self,db_data):
        self.id= db_data['id']
        self.customer= db_data['customer']
        self.location= db_data['location']
        self.needed_by= db_data['needed_by']
        self.item= db_data['item']
        self.scope= db_data['scope']
        self.created_at= db_data['created_at']
        self.updated_at= db_data['updated_at']
        self.user_id= db_data['user_id']
        self.sellers=[]

    @classmethod
    def save(cls,data):
        query = "INSERT INTO job (customer, location, needed_by, item, scope, user_id) Values (%(customer)s, %(location)s, %(needed_by)s, %(item)s, %(scope)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM job;'
        results = connectToMySQL(cls.db).query_db(query)
        jobs = []
        for row in results:
            jobs.append(cls(row))
        return jobs

    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM job  WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def update(cls,data):
        query = "UPDATE job SET customer = %(customer)s, location = %(location)s, needed_by = %(needed_by)s, item = %(item)s, scope = %(scope)s,  updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query= "DELETE FROM job WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_sales(cls,data):
        query = """SELECT * FROM user JOIN job on user.id
                = job.user_id ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        sellers = []
        for sales in results:
            sales_person = cls(sales)
            user_data = {
                "id" : sales['id'],
                "first_name": sales['first_name'],
                "last_name" : sales['last_name'],
                "email" : sales['email'],
                "password": sales['password'],
                "created_at": sales['created_at'],
                "updated_at": sales['updated_at']
            }
            sales_person.sellers = User(user_data)
            sellers.append(sales_person)
            print('user_data.first_name')
        return sellers

    @staticmethod
    def validate_sales(job):
        is_valid=True
        if len(job['customer']) <3:
            is_valid = False
            flash("name must be longer than 3 characters", "job")
        if len(job['location']) < 3:
            is_valid = False
            flash("location must be at least 3 characters", "job")
        if len(job['needed_by']) == 0:
            is_valid = False
            flash("Please put in a valid date", "job")
        if len(job['item']) < 3 :
            is_valid = False
            flash("Items must be longer than 3 characters. ", "job")
        if len(job['scope']) < 10:
            is_valid = False
            flash("scope must be at least 10 characters", "job")
        return is_valid