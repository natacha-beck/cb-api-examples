import requests
import json
import getpass

# Extract information from ./config.json
(base_url, login, password, s3_dp_id, uk_dp_id, group_id, directory_basename, file_browse_path, file_basename) = (None,None,None,None,None,None,None,None,None)

# Read JSON file ./config.json
try:
    with open('./config.json') as json_file:
        data = json.load(json_file)
        print(data)
        base_url                         = data['base_url']
        login                            = data['login']
        password                         = data['password']
        file_copy_ids                    = data['file_copy_ids']
        file_copy_bourreau_id            = data['file_copy_bourreau_id']
        file_copy_dp_id                  = data['file_copy_dp_id']
except:
    print("Error reading ./config.json")
    exit()

####################
# 1. login         #
####################

credentials = {
    'login': login,
    'password': password
}

# Create a session
session_response = requests.post(
    url = '/'.join([base_url, 'session']),
    data = credentials,
    headers = {'Accept': 'application/json'}
)

session_info = None
if session_response.status_code != requests.codes.ok:
    print('Login failed.')
    exit()
else:
    print('Login successful.')
    session_info = session_response.json()


user_id          = str(session_info['user_id'])
cbrain_api_token = session_info['cbrain_api_token']

api_headers = {
    'Content-Type': 'application/json',
    'Accept'      : 'application/json',
}

token_params = (
    ('cbrain_api_token', cbrain_api_token),
)

######################################
# 2. call bourreau/file_copy         #
######################################

print ("\n\n=== File copy via Bourreau ===\n")

file_copy_data = {
    "userfile_ids": file_copy_ids,
    "dataprovider_id": file_copy_dp_id,
}

file_copy_response = requests.post(
    url = '/'.join([base_url, 'bourreaux', file_copy_bourreau_id, 'file_copy']),
    headers = api_headers,
    params = token_params,
    data = json.dumps(file_copy_data)
)

if file_copy_response.status_code != requests.codes.ok:
    print('Files copy failed.')
    print(file_copy_response.text)
    exit()
else:
    print('Files copy successful.')
    print(file_copy_response.json())

