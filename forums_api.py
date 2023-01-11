from flask import jsonify
from database_conn import db_select, get_db_user_connection
from user_accounts import connection_to_db, format_response

def get_posts():
    try:
        all_posts = db_select(connection_to_db, "select max(username) as username, posts.id, title, posts.description, posts.user_id, likes, dislikes, posts.date_created, posts.date_updated, count(comments.id) as comment from posts left join comments on posts.id = comments.post_id join user_table on posts.user_id = user_table.id group by posts.id order by posts.date_created desc")
        return jsonify(all_posts), 200
    except:
        return format_response(500, 'error retrieving posts')


def post_item(json_data):
    data = json_data
    if(data[0]['title'] and data[0]['description'] and data[0]['user_id']):
        try:
            params = (data[0]['title'],data[0]['description'], data[0]['user_id'])
            insert_post_into_forum_table = db_select(connection_to_db, "insert into posts (title, description, user_id, date_created, date_updated) values (%s,%s,%s,current_timestamp, current_timestamp) returning 1", params)
            return  format_response(200, 'success data was added'), 200
        except:
            return format_response(500, 'error adding response in post_item')
    else:
        return format_response(400, 'One or more of the input fields are invalid')


def edit_post(json_data):
    data = json_data
    if(data[0]['title'] and data[0]['description'] and data[0]['post_id']):
        params = (data[0]['title'], data[0]['description'], data[0]['post_id'])
        check_for_post = db_select(connection_to_db,"select * from posts where id = %s", (data[0]['post_id'],))
        if(len(check_for_post) > 0):
            update_post = db_select(connection_to_db,"update posts set title=%s, description=%s, date_updated=current_timestamp where id =%s returning 1", params)
            return  format_response(200, 'success data was updated successfully'), 200
        else:
            return format_response(404, 'No post was found relating to ID given'), 404

def get_comments(data):
    params = (data[0]['post_id'],)
    try:
        get_comment_by_id = db_select(connection_to_db, "select comments.id, post_id, user_id, description, date_created, date_updated, user_table.username from comments join user_table on user_table.id = user_id where post_id = %s", params)
        return get_comment_by_id, 200
    except:
        return format_response(500, 'error retrieving comments')
    

def add_comment(json_data):
    data = json_data
    params = (data[0]['description'], data[0]['post_id'], data[0]['user_id'])
    try:
        add_comment_to_table = db_select(connection_to_db, "insert into comments (description, post_id, user_id, date_created, date_updated) values (%s,%s,%s, current_timestamp, current_timestamp) returning 1", params)
        return format_response(200, 'comment has been added successfully'),200
    except:
        return format_response(500, 'error adding comment')

def edit_comment(json_data):
    data = json_data
    params = (data[0]['description'], data[0]["comment_id"])
    check_item_result = check_item_exists('select * from comments where id = %s', (data[0]["comment_id"],))
    if(check_item_result ==  True):
        try:
            edit_comment = db_select(connection_to_db, "update comments set description=%s, date_updated=current_timestamp where id =%s returning 1", params)
            return format_response(200, 'comment updated successfully'), 200
        except:
            return format_response(500, 'failed to update comment')
    else:
        return check_item_result

def vote_on_post(data):
    params = (data[0]['post_id'],)
    try:
        if(data[0]['vote'] == 'upvote'):
            upvote_post = db_select(connection_to_db, "update posts set likes = likes + 1 where id = %s returning 1", params)
            return format_response(200, 'success post was up voted successfully'), 200
        elif(data[0]['vote'] == 'downvote'):
            upvote_post = db_select(connection_to_db, "update posts set dislikes = dislikes + 1 where id = %s returning 1", params)
            return format_response(200, 'success post was down voted successfully'), 200
    except:
        return format_response(500, 'unable to add vote to post')

def check_item_exists(query, param):
    check_for_item = db_select(connection_to_db,query, param)
    if(len(check_for_item) > 0):
        return True
    else:
        return format_response(404, 'item could not be found in database')