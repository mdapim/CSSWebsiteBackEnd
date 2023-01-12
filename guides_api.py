from database_conn import db_select, get_db_user_connection
from user_accounts import connection_to_db, format_response
from forums_api import validate_returned_query

def get_resources(): 
    try:
        category_list = db_select(connection_to_db, 'select * from categories')
        validate_category_list = validate_returned_query(category_list, 'error retrieving categories')

        resource_list = db_select(connection_to_db,'select * from resources')
        validate_resource_list = validate_returned_query(resource_list,'error retrieving resources')

        if (validate_category_list[1] != 500 and validate_resource_list[1] != 500):
            mapped_category_list = {}
            for i in category_list:
                mapped_category_list[i["category_id"]] = i["category_name"]

            return [mapped_category_list, resource_list], 200

        else:
            return [validate_category_list[0] if validate_category_list[1] == 500 else 'retrieved categories successfully',
                    validate_resource_list[0] if validate_resource_list[1] == 500 else 'retrieved resource list successfully'],500

    except:
        return format_response(500, 'error retrieving resources'),500

def add_resource(data): 
    try:
        if(data[0]['user_type'] != '1'):
            return format_response(401, "unauthorized access, user doesn't have required access rights ")

        confirm_category_id = db_select(connection_to_db,'select category_id from categories where LOWER(category_name) = LOWER(%s) and exists(select * from categories where LOWER(category_name)=LOWER(%s))', (data[0]['category_name'], data[0]['category_name']))
        if(len(confirm_category_id) <= 0):
            confirm_category_id = db_select(connection_to_db, 'insert into categories (category_name) values (%s) returning category_id;', (data[0]['category_name'],))

        validate_category_id = validate_returned_query(confirm_category_id,'error getting category id')
        if(validate_category_id[1] == 500):
            return validate_category_id
        else:
            params = (data[0]['resource_link'], data[0]['resource_description'], confirm_category_id[0]['category_id'])
            add_resource = db_select(connection_to_db, "insert into resources (resource_link, resource_description, resource_category_id) values (%s,%s,%s) returning 'successfully added resource'", params)
            return validate_returned_query(add_resource, 'error adding resource into resource list')
    except:
        return format_response(500, 'error adding resource into resource list')
