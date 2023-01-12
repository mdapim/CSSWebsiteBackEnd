import sys
sys.path.append('../')
import requests
import json
from flask import Flask,jsonify
app = Flask(__name__)
base_url = "https://csswebsitebackend-production.up.railway.app/"

from database_conn import *
from forums_api import *
from server import * 

"""
tests:

server.py:
    /forum_post
        - (GET) get_posts(data)
        - (POST) post_item(data)
        - (PATCH) edit_post(data)
        - (DELETE) delete_post(data)

    /forum_comment
        - (POST) add_comment(data)
        - (PATCH) edit_comment(data)
        - (DELETE) delete_comment(data)
    /get_comments
        - (POST) get_comments(data)
    /forum_vote
"""


def test_get_all_posts(): #will fail without a single post
    with app.app_context():
        response = requests.get(base_url+'/forum_post')
        assert response.status_code==200
        first_response = response.json()[0]
        contents = ['comment','date_created','description','dislikes','id','title','user_id']
        for content in contents:
            assert first_response.get(content)!=None


        pass
def test_item_post(): #will fail without a user existing of id=1
    item_to_post = json.dumps([{'title':'TESTING_BACKEND','description':'TEST_DESCRIP.','user_id':'1'}])
    with app.app_context():
        response = requests.post(base_url+'/forum_post',
         item_to_post,
         headers={"Content-type": "application/json"}
         )
        assert response.status_code==200

        assert response.json()[0]['?column?'].startswith('success')

    pass
def test_item_post_no_user():
    item_to_post = json.dumps([{'title':'TESTING_BACKEND','description':'TEST_DESCRIP.'}])
    with app.app_context():
        response = requests.post(base_url+'/forum_post',
         item_to_post,
         headers={"Content-type": "application/json"}
         )
        print(response.json())
        assert response.status_code==200
        assert response.json()[0]['status']==500

def test_item_post_error():
    pass
def test_item_edited():
    pass
def test_item_deleted():
    item_to_delete = json.dumps([{'user_id':'1','post_id':'1','user_type':1}])
    with app.app_context():
        response = requests.delete(base_url+'/forum_post',
        data=item_to_delete,
        headers={"Content-type": "application/json"})
        assert response.json()[0]['status']==404 #will fail, if there is no post_id=1
def test_item_deleted_error():
    pass
def test_add_comment():
    pass
def test_edit_comment():
    pass
def test_delete_comment():
    pass
def test_get_all_comments():
    pass


