from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

db = 'Propose_help'


class Product:

    db = 'Propose_help'

    def __init__ (self,db_data):
        self.id= db_data['id']
        self.product_name= db_data['product_name']
        self.part_number= db_data['part_number']
        self.product_info= db_data['product_info']
        self.price= db_data['price']
        self.install_time= db_data['install_time']
        self.inventory_on_hand= db_data['inventory_on_hand']
        self.inventory_needed= db_data['inventory_needed']
        self.created_at= db_data['created_at']
        self.updated_at= db_data['updated_at']
        self.user_id= db_data['user_id']
        self.products=[]

    @classmethod
    def save_product(cls,data):
        query = "INSERT INTO product (product_name, part_number, product_info, price, install_time, inventory_on_hand, inventory_needed, user_id) Values (%(product_name)s, %(part_number)s, %(product_info)s, %(price)s, %(install_time)s,  %(inventory_on_hand)s, %(inventory_needed)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def product_name(cls):
        query = 'SELECT product_name FROM product;'
        return connectToMySQL(cls.db).query_db(query)


    @classmethod
    def get_all_product(cls):
        query = 'SELECT * FROM product;'
        results = connectToMySQL(cls.db).query_db(query)
        products = []
        for row in results:
            products.append(cls(row))
        return products

    
    @classmethod
    def get_one_product(cls,data):
        query = "SELECT * FROM product  WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def update_product(cls,data):
        query = "UPDATE product SET product_name = %(product_name)s, part_number = %(part_number)s, product_info = %(product_info)s, price = %(price)s, install_time = %(install_time)s, starting_inventory = %(starting_inventory)s, inventory_on_hand = %(inventory_on_hand)s, inventory_needed = %(inventory_needed)s,  updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete_product(cls,data):
        query= "DELETE FROM product WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_products(cls,data):
        query = """SELECT * FROM user JOIN product on user.id
                = product.user_id ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        products = []
        for onhand in results:
            inventory = cls(onhand)
            product_data = {
                "id" : onhand['id'],
                "first_name": onhand['first_name'],
                "last_name" : onhand['last_name'],
                "email" : onhand['email'],
                "password": onhand['password'],
                "created_at": onhand['created_at'],
                "updated_at": onhand['updated_at']
            }
            inventory.products = User(product_data)
            products.append(inventory)
            print('user_data.first_name')
        return inventory

    @staticmethod
    def validate_products(product):
        is_valid=True
        if len(product['product_name']) <1:
            is_valid = False
            flash("name must be longer than 1 character", "product")
        if len(product['part_number']) == 0:
            is_valid = False
            flash("partnumber must be larger than 0", "product")
        if len(product['product_info']) <3:
            is_valid = False
            flash("product info must be longer than 3 characters", "product")
        if len(product['price']) == 0 :
            is_valid = False
            flash("Price must be larger than 0 ", "product")
        if len(product['install_time']) ==0:
            is_valid = False
            flash("install time must be longer than 0", "product")
        if len(product['inventory_on_hand']) ==0:
            is_valid = False
            flash("inventory on hand must be longer than 0", "product")
        if len(product['inventory_needed']) ==0:
            is_valid = False
            flash("inventory needed must be longer than 0", "product")
        return is_valid
    