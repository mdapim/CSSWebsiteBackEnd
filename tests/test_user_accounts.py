import sys
sys.path.append('../')
import requests
import json
from flask import Flask,jsonify
from string import ascii_lowercase
from random import randrange
app = Flask(__name__)
base_url = "https://csswebsitebackend-production.up.railway.app/"


def random_word() -> str:
    return ascii_lowercase[randrange(len(ascii_lowercase))]

def test_sign_up_user_already_in_database():
    data = [{"name": "hey",
"password":"hey"}]
    path = "/get_user"
    response = requests.post(url=base_url+"/create_user", headers={"Content-type": "application/json"},json= data)
    responseJson = json.loads(response.text)

    assert responseJson ==  [
    {
        "message": "Error creating account",
        "status": 500
    }
]

def test_sign_up_invalid_input_name():
    data = [{"name": "",
"password":"hey"}]
    path = "/get_user"
    response = requests.post(url=base_url+"/create_user", headers={"Content-type": "application/json"},json= data)
    responseJson = json.loads(response.text)
    
    assert responseJson ==  [
    {
        "message": "No inputs have been given",
        "status": 400
    }
]

def test_sign_up_invalid_input_password():
    data = [{"name": "hey",
"password":""}]
    path = "/get_user"
    response = requests.post(url=base_url+"/create_user", headers={"Content-type": "application/json"},json= data)
    responseJson = json.loads(response.text)
    
    assert responseJson ==  [
    {
        "message": "No inputs have been given",
        "status": 400
    }
]



def test_sign_up_successful():
    data = [{"name": str(random_word()),
"password":"12345"}]
    path = "/get_user"
    response = requests.post(url=base_url+"/create_user", headers={"Content-type": "application/json"},json= data)
    responseJson = json.loads(response.text)
    assert responseJson ==  [
    {
        "message": "user created",
        "status": 200
    }
    ]
    
    

def test_get_user_no_user_found_username_incorrect():
    data = [{"name": "missingName",
"password":"test4"}]
    path = "/get_user"
    response = requests.post(url=base_url+"find_user", headers={"Content-type": "application/json"},json= data)
    responseJson = json.loads(response.text)
    assert responseJson ==  [{'message': 'user was not found (locate_user_data)', 'status': 404}]

def test_get_user_no_user_found_password_incorrect():
    data = [{"name": "mikeel",
"password":"missingpassword"}]
    path = "/get_user"
    response = requests.post(url=base_url+"find_user", headers={"Content-type": "application/json"},json= data)
    responseJson = json.loads(response.text)
    assert responseJson ==  [{'message': 'user was not found (locate_user_data)', 'status': 404}]

def test_get_user_found():
    data = [{"name": "mikeel",
"password":"12345"}]
    path = "/get_user"
    response = requests.post(url=base_url+"find_user", headers={"Content-type": "application/json"},json= data)
    responseJson = json.loads(response.text)
    assert responseJson ==  [
    {
        "id": 12,
        "profile_picture": "https://api.dicebear.com/5.x/bottts/svg?seed=mikeel",
        "type_id": 2,
        "username": "mikeel"
    }
]


        


