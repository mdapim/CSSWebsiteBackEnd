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
        assert response.status_code==200
        assert response.json()[0]['status']==500

def test_item_post_error():
    pass
def test_item_edited():

    pass
def test_add_comment():
    comment_item = json.dumps([{'post_id':1,'description':'TEST_COMMENT','user_id':1}])
    with app.app_context():
        last_post = requests.get(base_url+'/forum_post').json()[0]
        comment_item = json.dumps([{'post_id':last_post['id'],'description':'TEST_COMMENT','user_id':last_post['user_id']}])
        response = requests.post(base_url +'/forum_comment',data=comment_item,headers={'Content-Type':'application/json'})
        assert response.status_code==200
        all_comments = requests.post(base_url+'/get_comments',data=json.dumps([{'post_id':last_post['id']}]),headers={'Content-Type':'application/json'}).json()[0]
        print(all_comments)
        assert all_comments['description']=='TEST_COMMENT'
    pass
def test_edit_comment():
    with app.app_context():
        last_post = requests.get(base_url+'/forum_post').json()[0]
        all_comments = requests.post(base_url+'/get_comments',data=json.dumps([{'post_id':last_post['id']}]),headers={'Content-Type':'application/json'}).json()[0]
        edited_text = 'TEST_COMMENT_EDITED'
        comment_id = all_comments['id']
        user_id = all_comments['user_id']
        data = json.dumps([{'user_id':user_id,'comment_id':comment_id,'description':edited_text}])
        edited_comment_message = requests.patch(base_url+'/forum_comment',data=data,headers={'Content-Type':'application/json'}).json()
        print(edited_comment_message)
        edited_comments = requests.post(base_url+'/get_comments',data=json.dumps([{'post_id':last_post['id']}]),headers={'Content-Type':'application/json'}).json()[0]
        assert edited_comments.get('description')!=None
        assert edited_comments.get('description')=='TEST_COMMENT_EDITED'
def test_delete_comment_user():
        last_post = requests.get(base_url+'/forum_post').json()[0]
        all_comments = requests.post(base_url+'/get_comments',data=json.dumps([{'post_id':last_post['id']}]),headers={'Content-Type':'application/json'}).json()[0]
        comment_id = all_comments['id']
        user_id = all_comments['user_id']
        data = json.dumps([{'comment_id':comment_id,'user_id':user_id,'user_type':2}])
        response = requests.delete(base_url+'/forum_comment',data=data,headers={'Content-Type':'application/json'})
        all_comments = requests.post(base_url+'/get_comments',data=json.dumps([{'post_id':last_post['id']}]),headers={'Content-Type':'application/json'}).json()
        print(response.json())
        print(all_comments)
        assert len(all_comments)==0
        assert response.json()[0].get('?column?')!=None
def test_delete_any_comment_admin():
    test_item_post()
    test_add_comment()
    last_post = requests.get(base_url+'/forum_post').json()[0]
    all_comments = requests.post(base_url+'/get_comments',data=json.dumps([{'post_id':last_post['id']}]),headers={'Content-Type':'application/json'}).json()[0]
    comment_id = all_comments['id']
    user_id = 5 #an admin account
    data = json.dumps([{'comment_id':comment_id,'user_id':user_id,'user_type':1}])
    response = requests.delete(base_url+'/forum_comment',data=data,headers={'Content-Type':'application/json'})
    new_comments =  requests.post(base_url+'/get_comments',data=json.dumps([{'post_id':last_post['id']}]),headers={'Content-Type':'application/json'}).json()
    print(new_comments)
    assert len(new_comments)==0

    

    pass
def test_post_deleted():
        last_post = requests.get(base_url+'/forum_post').json()[0]
        item_to_delete = json.dumps([{'user_id':last_post['user_id'],'post_id':last_post['id'],'user_type':last_post['user_id']}])
        response = requests.delete(base_url+'/forum_post',
        data=item_to_delete,
        headers={"Content-type": "application/json"})
        print(response.json()[0])
        assert response.json()[0].get('?column?')=='post has been deleted successfully'


