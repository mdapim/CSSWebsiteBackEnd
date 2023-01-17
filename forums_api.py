from flask import jsonify
from database_conn import db_select, get_db_user_connection
from user_accounts import connection_to_db, format_response

def get_all_comments(): 
    all_comments = db_select(connection_to_db, 'select date_created, date_updated, description, comments.id, post_id, user_id, username,profile_picture from comments join user_table on user_id = user_table.id order by id desc')
    return validate_returned_query(all_comments, 'error retrieving comments')

def get_posts(): 
        all_posts = db_select(connection_to_db, "select max(username) as username,max(profile_picture) as profile_picture, posts.id, title, posts.description, posts.user_id, likes, dislikes, posts.date_created, posts.date_updated, count(comments.id) as comment from posts left join comments on posts.id = comments.post_id join user_table on posts.user_id = user_table.id group by posts.id order by posts.date_created desc")
        return validate_returned_query(all_posts, 'error retrieving posts')


def post_item(data): 
    try:
        if(data[0]['title'] and data[0]['description'] and data[0]['user_id']):
            params = (data[0]['title'],data[0]['description'], data[0]['user_id'], data[0]['code'])
            insert_post_into_forum_table = db_select(connection_to_db, "insert into posts (title, description, user_id, date_created, date_updated, code) values (%s,%s,%s,current_timestamp, current_timestamp, %s) returning (id,'success')", params)
            return validate_returned_query(insert_post_into_forum_table, 'error adding response in post_item')

        else:
            return format_response(400, 'One or more of the input fields are invalid'),400

    except:
        return format_response(500, 'error adding response in post_item')


def edit_post(data): 
    try:
        params = (data[0]['title'], data[0]['description'], data[0]['post_id'])
        check_for_post_result = check_item_exists("select * from posts where id = %s and user_id = %s", (data[0]['post_id'], data[0]['user_id']))

        if(check_for_post_result == True):
            update_post = db_select(connection_to_db,"update posts set title=%s, description=%s, date_updated=current_timestamp where id =%s returning 'success data was updated successfully'", params)
            return  validate_returned_query(update_post, 'error updating post')

        else:
            return check_for_post_result

    except:
        return format_response(500, 'error updating post')

def delete_post(data): 
    try:
        check_for_post_and_user_validation = db_select(connection_to_db, "select * from posts where id = %s and (user_id = %s or 1 = %s)", (data[0]['post_id'],data[0]['user_id'],data[0]['user_type']))
        check_query_execution = validate_returned_query(check_for_post_and_user_validation, 'error checking for post and user access')
        
        if(check_query_execution[1] == 500):
            return check_query_execution
        
        if(len(check_for_post_and_user_validation) <= 0):
            return format_response(404, 'item has already been deleted or user does not have required access')

        params = (data[0]['post_id'],data[0]['post_id'],data[0]['user_id'],data[0]['user_type'])
        delete_comments = db_select(connection_to_db, "delete from comments where post_id = %s and exists(select post_id, posts.user_id from comments join posts on posts.id = post_id where post_id = %s  and (posts.user_id = %s or 1=%s)) returning 'comments deleted successfully'", params)
        check_comments_are_deleted = validate_returned_query(delete_comments, 'error checking for comments related to post, unable to delete post')

        if(check_comments_are_deleted[1] != 500):
            delete_item = db_select(connection_to_db, "delete from posts where id = %s and exists(select * from posts where id = %s and (user_id = %s or 1 = %s)) returning 'post has been deleted successfully'", params)
            return validate_returned_query(delete_item,'Error deleting post, related comments deleted')

        return check_comments_are_deleted

    except:
        return format_response(500, 'error deleting posts')

def get_comments(data):   
    try:
        params = (data[0]['post_id'],)
        get_comment_by_id = db_select(connection_to_db, "select comments.id, post_id, user_id, description, date_created, date_updated, user_table.username from comments join user_table on user_table.id = user_id where post_id = %s", params)
        return validate_returned_query(get_comment_by_id, 'Error retrieving comments')

    except:
        return format_response(500, 'error retrieving comments')
    

def add_comment(data): 
    try:
        check_item_result = check_item_exists('select * from posts where id = %s', (data[0]['post_id'],))

        if(check_item_result == True):
            if (data[0]['description'] and data[0]['post_id'] and data[0]['user_id']):
                params = (data[0]['description'], data[0]['post_id'], data[0]['user_id'])
                add_comment_to_table = db_select(connection_to_db, "insert into comments (description, post_id, user_id, date_created, date_updated) values (%s,%s,%s, current_timestamp, current_timestamp) returning 'comment has been added successfully'", params)
                return validate_returned_query(add_comment_to_table,'error adding comment')

            else:
                return format_response(400, 'One or more of the input fields are invalid'),400

        else:
                return format_response(404, 'No Post has been found to comment'), 404
    except:
        return format_response(500, 'error adding comment')

def edit_comment(data):
    try:
        params = (data[0]['description'], data[0]["comment_id"], data[0]["comment_id"])
        check_item_result = check_item_exists('select * from comments where id = %s and user_id = %s', (data[0]["comment_id"], data[0]['user_id']))

        if(check_item_result ==  True):
                edit_comment = db_select(connection_to_db, "update comments set description=%s, date_updated=current_timestamp where id =%s and exists(select * from comments where id = %s) returning 'comment updated successfully'", params)
                return validate_returned_query(edit_comment, 'error updating comment')

        else:
            return check_item_result

    except:
        return format_response(500, 'error updating comment')

def delete_comment(data):
    try:
        params = (data[0]['comment_id'],data[0]['comment_id'], data[0]['user_id'], data[0]['user_type'])
        delete_item = db_select(connection_to_db, "delete from comments where id = %s and exists(select * from comments where id = %s and (user_id = %s or 1 = %s)) returning 'successfully deleted comment'", params)

        if(len(delete_item) <= 0):
            return format_response(404, 'item has already been deleted or user does not have required access')

        return validate_returned_query(delete_item, 'error deleting comment')

    except:
        return format_response(500, 'error deleting comment')

def vote_on_post(data):
    try:
        params = (data[0]['post_id'],)
        if(data[0]['vote'] == 'upvote'):
            upvote_post = db_select(connection_to_db, "update posts set likes = likes + 1 where id = %s returning 'success post was up voted successfully'", params)
            return validate_returned_query(upvote_post, 'error adding vote to post')

        elif(data[0]['vote'] == 'downvote'):
            downvote_post = db_select(connection_to_db, "update posts set dislikes = dislikes + 1 where id = %s returning 'success post was down voted successfully'", params)
            return validate_returned_query(downvote_post, 'error adding vote to post')

        else:
            return format_response(400, 'error adding vote to post - upvote / downvote not detected'),400

    except:
        return format_response(500, 'error adding vote to post')





def check_item_exists(query, param):
    check_for_item = db_select(connection_to_db,query, param)

    if(len(check_for_item) > 0):
        return True

    else:
        return format_response(404, 'item could not be found in database, or user has no access to item')

def validate_returned_query(returned_data, msg):
    if(returned_data in ['Error executing query.','No connection']):
        return format_response(500, msg + ' - ' + returned_data ), 500

    else:
        return returned_data, 200