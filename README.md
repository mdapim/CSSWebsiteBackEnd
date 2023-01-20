# CSSWebsiteBackEnd

# Introduction to the BackEnd
The BackEnd for Style Studios uses Flask to create API's to communicate with a Hosted postgresql server on elephantSQL. The user information, forum posts, sessions and guide links are stored on the database in tables. The server is then hosted using Railway for automatic deployment when any changes are pushed to main.

CheckOut Live running server: https://csswebsitebackend-production.up.railway.app

## API EndPoints:

**/create_user ||
POST -> create new user in the user_tables ||
data to send -> [{"name": " ", "password":" "}]**

**/find_user ||
POST = -> find the user from the user_tables ||
data to send -> [{"name": " ", "password":" "}]**

**/forum_post**

GET -> gets all forum post**

**POST -> add a new post to posts table ||
data to send -> [{"title":" ", "description":" ", "user_id":" ", "code":" ", "category":" "}]**

**EDIT -> update a row in posts table ||
data to send -> [{"title":" ", "description":" ", "post_id":"", "user_id":" "}]**

**DELETE -> delete a row in posts table (user type of 1 is an admin account) || 
data to send -> [{"post_id":"", "user_id":"", "user_type":""}]**

**/get_comments ||
POST -> get comment by postid ||
data to send -> [{"post_id": ""}]**

**/get_all ||
GET-> get all comments**

**/forum_comment**

**POST -> add a new comment to comments table ||
data to send -> [{"description":"", "post_id":"", "user_id":""}]**

**EDIT -> update a row in comments table ||
data to send -> [{"description":"", "comment_id":"", "user_id":""}]**

**DELETE -> delete a row in comments table (user type of 1 is an admin account) ||
data to send -> [{"comment_id":51, "user_id":"1", "user_type":"1"}]**

**/forum_vote ||
POST -> add a new vote to the table vote has to be either ('downvote' or 'upvote') ||
data to send -> [{"post_id":"", "vote":""}]**

**/guides_links**

**GET -> return all resources from resource table**

**POST -> add a resource to the tables (need an admin user type of 1) ||
data to send -> [{"resource_description":"","resource_link":"","category_name":"","user_type":"1"}]**

**/add_click**

**POST -> increment click counter for guide links ||
data to send -> [{"resource_id": "1"}]**

## Tables created and used in elephantsql:

- categories (store categories for resources)
- comments (store comments)
- forum_categories (store forum categories)
- posts (store forum posts)
- resources (store helpful sites)
- sessions (store user sessions)
- user_table (store user data )
- user_types (store user types)

# Flask
Flask is a micro web framework written in Python. It is classified as a micro-framework because it does not require particular tools or libraries.[2] It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions.

## Features:

- Development Sever and Debugger
- Integrated support for unit testing
- Supports for secure cookies
- complete documentation

# Elephant SQL
ElephantSQL is a PostgreSQL database hosting service.

## Features:

- Manage administrative tasks of Postgresql (installation and upgrades)
- integrated with several cloud application platforms

# Railway:
Railway is an infrastructure platform where you can provision infrastructure, develop with that infrastructure locally, and then deploy to the cloud.

## Features:

- Automated deployment
- Secrets management
- Railway command line interface, allows you to connect from any terminal in the world

# Installation and Running the Code

Download/clone project repository to your local directory:
git clone https://github.com/mdapim/CSSWebsiteBackEnd.git

Create a virtual environment:
python3 -m venv venv

Start the virtual environment:
. venv/bin/activate

Install required files:
pip3 install -r requirements.txt

Add .env file:
create a file called .env in the root folder
within this you will need to add the following details taken from ElephantSQL ->
PASS=(for the database password please ask github team)
HOST=mel.db.elephantsql.com
DBNAME=nspyhbjz

Start the server:
python3 server.py

Run the tests for the APIS:
navigate to test folders and type the command
pytest test_user_accounts.py
pytest test_forums.py

# Documentation

## BackEnd Technologies:

- Flask
- Postgresql version 13.9
- ElephantSQL (Hosting Database)

## Testing:

- Pytest

## Authors

- **CALLUM HALL** - [Callum3574](https://github.com/Callum3574)
- **MICHAEL APIM** [mdapim](https://github.com/mdapim)
- **ADAM LAKER ILLOU** - [Ademsk1](https://github.com/Ademsk1)
