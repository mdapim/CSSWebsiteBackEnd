from flask import Flask, current_app, jsonify, request, json
from flask_cors import CORS
from database_conn import *
from user_accounts import * 
from forums_api import *
from guides_api import *
from sessions_api import *
from datetime import datetime,timedelta

app = Flask(__name__)
CORS(app, origins=['https://lucky-madeleine-7ddeef.netlify.app', 'https://idyllic-rabanadas-35e31a.netlify.app','http://localhost:3000'],supports_credentials=True)

@app.route('/', methods=['GET'])
def home():
    cookies = request.cookies.get('s5s__uuid')
    if cookies:
        user_data = get_sessions(cookies)
        return jsonify(user_data),200
    else:
        return jsonify('NO COOKIES'),404

@app.route('/create_user', methods=['POST'])
def creating_user():
    data = request.json
    return create_new_user(data)


@app.route('/find_user', methods=['POST', 'GET'])
def finding_user():
    data = request.json
    located_user = locate_user_data(data)
    uuid = create_session(located_user[0])
    jsonified_located_user = jsonify(located_user)
    expiry_date = datetime.utcnow()+timedelta(days=1)
    expiry_date = expiry_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
    jsonified_located_user.set_cookie('s5s__uuid',uuid,expires=expiry_date)
    return jsonified_located_user


@app.route('/all_users_details', methods=['GET'])
def gather_all_user_details():
    return get_all_user_info()


@app.route('/forum_post', methods=['GET','POST','PATCH', 'DELETE'])
def forum_actions():
    if(request.method == 'GET'):
        return get_posts()
    elif(request.method == 'POST'):
        return post_item(request.json)
    elif(request.method == 'PATCH'):
        return edit_post(request.json)
    elif(request.method == 'DELETE'):
        return delete_post(request.json)

@app.route('/forum_comment', methods=['POST', 'PATCH', 'DELETE'])
def comments_actions():
    if(request.method == 'POST'):
        return add_comment(request.json)
    elif(request.method == 'PATCH'):
        return edit_comment(request.json)
    elif(request.method == 'DELETE'):
        return delete_comment(request.json)

@app.route('/get_comments', methods=['POST'])
def get_comment_by_id():
    if(request.method == 'POST'):
        data = request.json
        return get_comments(data)

@app.route('/forum_vote', methods=['POST'])
def voting_actions():
    data = request.json
    return vote_on_post(data)

@app.route('/get_all')
def getting_all_comment():
    return get_all_comments()


@app.route('/guides_links', methods=['GET','POST'])
def add_link_to_resources():
    if(request.method == 'GET'):
        return get_resources()
    if(request.method == 'POST'):
        data = request.json
        return add_resource(data)
 




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=get_port()) 
