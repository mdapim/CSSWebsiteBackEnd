import uuid
import bcrypt
from flask import jsonify,request
from database_conn import db_select, get_db_user_connection
from user_accounts import connection_to_db, format_response,create_hash_password,compare_hashed_passwords


def get_sessions(user_uuid):
    search_matching_uuid = 'SELECT * FROM sessions WHERE uuid=%s'
    find_user_query = 'SELECT * FROM user_table WHERE id=%s'
    sql_response = db_select(connection_to_db,search_matching_uuid,(user_uuid,))[0]
    if (type(sql_response)!=str):
        #match
        print(sql_response['user_id'])
        user_details = db_select(connection_to_db,find_user_query,(sql_response['user_id'],))[0]
        user_info = [{'id':user_details['id'],'username':user_details['username'],'user_type':user_details['type_id'],'profile_picture':user_details['profile_picture']}]
        return user_info
    else:
        return 'TIMEDOUT'
def create_session(data):
    create_session_query = 'INSERT INTO sessions (uuid,created_at,user_id) VALUES (%s,CURRENT_TIMESTAMP,%s) RETURNING 1'
    user_uuid = str(uuid.uuid4())
    params = (user_uuid, int(data[0]['id']))
    sql_response = db_select(connection_to_db,create_session_query,params)
    return user_uuid

def delete_session(data):

    pass
