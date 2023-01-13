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

    response = requests.get(base_url+'/forum_post')
    assert response.status_code==200
    first_response = response.json()[0]
    contents = ['comment','date_created','description','dislikes','id','title','user_id']
    for content in contents:
        assert first_response.get(content)!=None

def test_item_post(): #will fail without a user existing of id=1
    item_to_post = json.dumps([{'title':'TESTING_BACKEND','description':'TEST_DESCRIP.','user_id':'1'}])
    
    response = requests.post(base_url+'/forum_post',
        item_to_post,
        headers={"Content-type": "application/json"}
        )
    assert response.status_code==200
    assert response.json()[0]['?column?'].startswith('success')

    pass
def test_item_post_no_user():
    item_to_post = json.dumps([{'title':'TESTING_BACKEND','description':'TEST_DESCRIP.'}])
    response = requests.post(base_url+'/forum_post',
        item_to_post,
        headers={"Content-type": "application/json"}
        )
    assert response.status_code==200
    assert response.json()[0]['status']==500


def test_item_edited():
    item_to_edit = requests.get(base_url+'/forum_post').json()[0]
    edit_request = json.dumps([{'title':'TEST_EDIT_TITLE','description':'EDITED_DESCRIPTION','user_id':1,'post_id':item_to_edit['id']}])
    response = requests.patch(base_url+'/forum_post',data=edit_request,headers={'Content-Type':'application/json'})
    item_edited = requests.get(base_url+'/forum_post').json()[0]
    assert response.json()[0].get('?column?')!=None
    assert response.json()[0].get('?column?').startswith('success')
    assert item_edited.get('description')=='EDITED_DESCRIPTION'
    
def test_add_comment():
    last_post = requests.get(base_url+'/forum_post').json()[0]
    comment_item = json.dumps([{'post_id':last_post['id'],'description':'TEST_COMMENT','user_id':last_post['user_id']}])
    response = requests.post(base_url +'/forum_comment',data=comment_item,headers={'Content-Type':'application/json'})
    assert response.status_code==200
    all_comments = requests.post(base_url+'/get_comments',data=json.dumps([{'post_id':last_post['id']}]),headers={'Content-Type':'application/json'}).json()[0]
    assert all_comments['description']=='TEST_COMMENT'

def test_edit_comment():
    last_post = requests.get(base_url+'/forum_post').json()[0]
    all_comments = requests.post(base_url+'/get_comments',data=json.dumps([{'post_id':last_post['id']}]),headers={'Content-Type':'application/json'}).json()[0]
    edited_text = 'TEST_COMMENT_EDITED'
    comment_id = all_comments['id']
    user_id = all_comments['user_id']
    data = json.dumps([{'user_id':user_id,'comment_id':comment_id,'description':edited_text}])
    edited_comment_message = requests.patch(base_url+'/forum_comment',data=data,headers={'Content-Type':'application/json'}).json()
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
        assert len(all_comments)==0
        assert response.json()[0].get('?column?')!=None
def test_upvote_downvote():
    last_post = requests.get(base_url+'/forum_post').json()[0]
    data_upvote = json.dumps([{'vote':'upvote','user_id':5,'post_id':last_post['id']}])
    data_downvote = json.dumps([{'vote':'downvote','user_id':5,'post_id':last_post['id']}])
    response_up = requests.post(base_url+'/forum_vote',data=data_upvote,headers={'Content-Type':'application/json'})
    response_down = requests.post(base_url+'/forum_vote',data=data_downvote,headers={'Content-Type':'application/json'})
    last_post_updated = requests.get(base_url+'/forum_post').json()[0]
    assert last_post_updated['likes']==last_post['likes']+1
    assert last_post_updated['dislikes']==last_post['dislikes']+1

def test_post_deleted():
    last_post = requests.get(base_url+'/forum_post').json()[0]
    item_to_delete = json.dumps([{'user_id':last_post['user_id'],'post_id':last_post['id'],'user_type':last_post['user_id']}])
    response = requests.delete(base_url+'/forum_post',
    data=item_to_delete,
    headers={"Content-type": "application/json"})
    assert response.json()[0].get('?column?')=='post has been deleted successfully'


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
    assert len(new_comments)==0
