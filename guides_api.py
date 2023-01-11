from database_conn import db_select, get_db_user_connection
from user_accounts import connection_to_db, format_response

def get_resources():
    category_list = db_select(connection_to_db, 'select * from categories')

    resource_list = db_select(connection_to_db,'select * from resources')

    mapped_category_list = []
    for i in category_list:
        mapped_category_list.append({i["category_id"]:i["category_name"]})
    return [mapped_category_list, resource_list]

def add_resource(data):

    confirm_category_id = db_select(connection_to_db,'select category_id from categories where LOWER(category_name) = LOWER(%s) and exists(select * from categories where LOWER(category_name)=LOWER(%s))', (data[0]['category_name'], data[0]['category_name']))
    if(len(confirm_category_id) <= 0):
        confirm_category_id = db_select(connection_to_db, 'insert into categories (category_name) values (%s) returning category_id;', (data[0]['category_name'],))
    params = (data[0]['resource_link'], data[0]['resource_description'], confirm_category_id[0]['category_id'])
    add_resource = db_select(connection_to_db, "insert into resources (resource_link, resource_description, resource_category_id) values (%s,%s,%s) returning 'added'", params)
    
    return add_resource
