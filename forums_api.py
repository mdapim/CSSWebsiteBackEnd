from database_conn import db_select, get_db_user_connection
from user_accounts import connection_to_db, format_response

def get_posts():
    try:
        all_posts = db_select(connection_to_db, "select posts.id, title, posts.description, posts.user_id, likes, dislikes, posts.date_created, posts.date_updated, count(comments.id) as comment from posts left join comments on posts.id = comments.post_id group by posts.id order by posts.date_created desc;")
        return all_posts, 200
    except:
        return format_response(500, 'error adding response in post_item')

def post_item(data):
    if(data[0]['title'] and data[0]['description'] and data[0]['user_id']):
        try:
            params = (data[0]['title'],data[0]['description'], data[0]['user_id'])
            insert_post_into_forum_table = db_select(connection_to_db, "insert into posts (title, description, user_id, date_created, date_updated) values (%s,%s,%s,current_timestamp, current_timestamp) returning 1", params)
            return  format_response(200, 'success data was added'), 200
        except:
            return format_response(500, 'error adding response in post_item')
    else:
        return format_response(400, 'One or more of the input fields are invalid')

def edit_post():
    pass

def add_comment():
    pass

def edit_comment():
    pass

def upvote_post():
    pass

def downvote_post():
    pass