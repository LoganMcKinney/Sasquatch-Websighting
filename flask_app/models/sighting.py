from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL

from flask_app import app
from flask import flash
from flask_app.models import user

class Sighting:
    db = "Sasquatch"
    def __init__(self, sighting):
        self.id = sighting['id']
        self.location = sighting['location']
        self.discription = sighting['discription']
        self.sighting_date = sighting['sighting_date']
        self.number_of = sighting['number_of']
        self.created_at = sighting['created_at']
        self.updated_at = sighting['updated_at']
        self.user_id = sighting['user_id']
        self.user = None

    @classmethod
    def create_sighting(cls, sighting):
        if not cls.validate_sighting(sighting):
            return False
        query = """
        INSERT INTO sightings (location, discription, sighting_date, number_of, created_at, updated_at, user_id)
        VALUES (%(location)s, %(discription)s, %(sighting_date)s, %(number_of)s, NOW(), NOW(), %(user_id)s)
        ;"""
        sighting_id = connectToMySQL(cls.db).query_db(query, sighting)
        sighting = cls.get_sighting_by_id(sighting_id)
        return sighting

    @classmethod
    def get_sighting_by_id(cls, sighting_id):
        data = { "id" : sighting_id}
        query = """
        SELECT sightings.id, location, discription, sighting_date, number_of, sightings.created_at, sightings.updated_at,
        users.id as user_id, first_name, last_name, email, password, users.created_at as ca, users.updated_at as ua
        FROM sightings
        JOIN users on users.id = sightings.user_id
        WHERE sightings.id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        result = result[0]
        sightings = cls(result)
        sightings.user = user.User(
                    {
            "id" : result['user_id'],
            "first_name" : result['first_name'],
            "last_name" : result['last_name'],
            "email" : result['email'],
            "password" : result['password'],
            "created_at" : result['ca'],
            "updated_at" : result['ua']
            }
        )
        return sightings

    @classmethod
    def get_all_sightings(cls):
        query = """
        SELECT sightings.id, location, discription, sighting_date, number_of, sightings.created_at, sightings.updated_at,
        users.id as user_id, first_name, last_name, email, password, users.created_at as ca, users.updated_at as ua
        FROM sightings
        JOIN users on users.id = sightings.user_id
        ;"""
        sighting_data = connectToMySQL(cls.db).query_db(query)
        sightings = []
        for sighting in sighting_data:
            sighting_obj = cls(sighting)
            sighting_obj.user = user.User(
                    {
            "id" : sighting['user_id'],
            "first_name" : sighting['first_name'],
            "last_name" : sighting['last_name'],
            "email" : sighting['email'],
            "password" : sighting['password'],
            "created_at" : sighting['ca'],
            "updated_at" : sighting['ua']
            }
            )
            sightings.append(sighting_obj)
        return sightings

    @classmethod
    def update_sighting(cls, sighting_edit, session_id):
        sighting = cls.get_sighting_by_id(sighting_edit['id'])
        if sighting.user.id != session_id:
            flash("You must be the creator to edit.")
            return False
        if not cls.validate_sighting(sighting_edit):
            return False
        query = """
        UPDATE sightings
        SET location = %(location)s, discription = %(discription)s, 
        sighting_date = %(sighting_date)s, number_of = %(number_of)s, updated_at = NOW()
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, sighting_edit)
        sighting = cls.get_sighting_by_id(sighting_edit['id'])
        return sighting

    @classmethod
    def delete_sighting(cls, sighting_id):
        data = { "id" : sighting_id }
        query = """
        DELETE FROM sightings
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return sighting_id

    @staticmethod
    def validate_sighting(sighting):
        is_vlaid = True
        if len(sighting['location']) < 3:
            is_vlaid = False
            flash('Location must be at least 3 characters long.')
        if len(sighting['discription']) < 3:
            is_vlaid = False
            flash('Discription must be at least 3 characters long.')
        if len(sighting['sighting_date']) <= 0:
            is_vlaid = False
            flash('Date required.')
        if sighting['number_of'] <= "0":
            is_vlaid = False
            flash('Number of sasquatches must be greater than 0.')

        return is_vlaid

