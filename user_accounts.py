
from flask import Flask, jsonify, request, json
from flask_cors import CORS
import requests
import bcrypt
from database_conn import db_select, get_db_user_connection

connection_to_db = get_db_user_connection()

def create_new_user(data): #handle empty input
    print(data)
    if(data[0]['name']=='' or data[0]['password']==''):
        return format_response(400, 'No inputs have been given')
    all_user_table_info = db_select(connection_to_db, 'select * from user_table')
    try:
        if not any(dictionary.get('username') == data[0]['name'] and compare_hashed_passwords(data[0]['password'], dictionary.get('salt'), dictionary.get('password')) for dictionary in all_user_table_info):
            hashed_result = (create_hash_password(data[0]['password']))
            send = db_select(connection_to_db, 'insert into user_table (username, password) values (%s, %s) returning 1', ((data[0]['name']),(hashed_result[0])))
            return format_response(200, 'user created')
        else:
            return format_response(400,'user is already in database')
    except:
        return format_response(500, 'Error creating account')


def locate_user_data(data):
    try:
        all_user_table_info = db_select(connection_to_db, 'select * from user_table')
        for user in all_user_table_info:
            if(user['username'] == data[0]['name'] and compare_hashed_passwords(data[0]['password'], user.get('salt'), user.get('password'))):
                selected_user = db_select(connection_to_db, 'select * from user_table where username=%s and password=%s', ((user['username']),(user['password'])))
                return jsonify(selected_user), 200
        return format_response(404,'user was not found'), 404
    except:
        return format_response(500, 'Error Fetching User'), 500


def get_all_user_info():
    all_user_table_info = db_select(connection_to_db, 'select * from user_table')
    return jsonify(all_user_table_info)

def create_hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('UTF-8'), salt)
    return([hashed.decode('UTF-8'),salt.decode('UTF-8')])


def compare_hashed_passwords(inputted_password, saved_password):
    return bcrypt.checkpw(inputted_password.encode('UTF-8'), saved_password.encode('UTF-8'))

def format_response(code, message):
    return [{"status": code, "message": message}]