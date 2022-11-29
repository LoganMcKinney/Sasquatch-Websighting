from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL

from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class User:
    db = "Sasquatch"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_user(cls, data):
        if not cls.validate_user_reg_data(data):
            return False
        data = cls.parse_reg_data(data)
        query = """
        INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query, data)
        session['user_id'] = user_id
        session['user_name'] = f"{data['first_name']} {data['last_name']}"
        return True 

    @classmethod
    def get_user_by_email(cls, email):
        data = { 'email' : email }
        query = """
        SELECT * 
        FROM users
        WHERE email = %(email)s
        ;"""
        result = MySQLConnection(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result

    @classmethod
    def get_user_by_id(cls, user_id):
        data = { 'id' : user_id }
        query = """
        SELECT * 
        FROM users
        WHERE id = %(id)s
        ;"""
        result = MySQLConnection(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result


    @staticmethod
    def validate_user_reg_data(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 3:
            is_valid = False
            flash('First name must be at least 3 characters long.')
        if len(data['last_name']) < 3:
            is_valid = False
            flash('Last name must be at least 3 characters long.')
        if len(data['password']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters long')
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Please use valid email address.')
        if User.get_user_by_email(data["email"]):
            is_valid = False
            flash('That email is already in use')
        if data['password'] != data['confirm_password']:
            is_valid = False
            flash('Passwords do not match')
        return is_valid

    @staticmethod
    def parse_reg_data(data):
        parse_data = {}
        parse_data['email'] = data['email']
        parse_data['first_name'] = data['first_name']
        parse_data['last_name'] = data['last_name']
        parse_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parse_data

@staticmethod
def login_user(data):
    this_user = User.get_user_by_email(data['email'])
    if this_user:
        if bcrypt.check_password_hash(this_user.password, data['password']):
            session['user_id'] = this_user.id
            session['user_name'] = f"{this_user.first_name} {this_user.last_name}"
            return True
    flash("Email or Password incorrect")
    return False