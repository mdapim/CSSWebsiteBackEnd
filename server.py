from flask import Flask, current_app, jsonify, request, json
from flask_cors import CORS
from database_conn import *
from user_accounts import * 
from forums_api import *


app = Flask(__name__)
CORS(app, origins=['https://lucky-madeleine-7ddeef.netlify.app', 'http://localhost:3000'])

@app.route('/create_user', methods=['POST'])
def creating_user():
    data = request.json
    return create_new_user(data)


@app.route('/find_user', methods=['POST', 'GET'])
def finding_user():
    data = request.json
    print(data)
    return locate_user_data(data)


@app.route('/all_users_details', methods=['GET'])
def gather_all_user_details():
    return get_all_user_info()


@app.route('/forum_post')
def forum_actions():
    
    if(request.method == 'GET'):
        return get_posts()
    elif(request.method == 'POST'):
        data = request.json
        return post_item(data)
    elif(request.method == 'PATCH'):
        return edit_post(data)

@app.route('/forum_comment', methods=['POST', 'PATCH'])
def comments_actions():
    data = request.json
    if(request.method == 'POST'):
        add_comment(data)
    elif(request.method == 'PATCH'):
        edit_comment(data)

@app.route('/forum_vote', methods=['POST'])
def voting_actions():
    data = request.json
    if(data[0] == 'upvote'):
        upvote_post(data)
    elif(data[0] == 'downvote'):
        downvote_post(data)

 




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=get_port() )
