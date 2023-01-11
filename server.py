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


@app.route('/forum_post', methods=['GET','POST','PATCH'])
def forum_actions():
    if(request.method == 'GET'):
        return get_posts()
    elif(request.method == 'POST'):
        return post_item(request.json)
    elif(request.method == 'PATCH'):
        return edit_post(request.json)

@app.route('/forum_comment', methods=['POST', 'PATCH'])
def comments_actions():
    if(request.method == 'POST'):
        return add_comment(request.json)
    elif(request.method == 'PATCH'):
        return edit_comment(request.json)

@app.route('/get_comments', methods=['POST'])
def get_comment_by_id():
    if(request.method == 'POST'):
        data = request.json
        return get_comments(data)

@app.route('/forum_vote', methods=['POST'])
def voting_actions():
    data = request.json
    return vote_on_post(data)


 




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')# port=get_port()
