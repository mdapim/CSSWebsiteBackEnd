from flask import Flask, current_app, jsonify, request, json
from flask_cors import CORS
from database_conn import *
from user_accounts import * 


app = Flask(__name__)
CORS(app, origins='http://localhost:3000')

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

 




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port = get_port() )
