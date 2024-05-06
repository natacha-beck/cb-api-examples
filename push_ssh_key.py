import requests
import json

(base_url, login, password, s3_dp_id, uk_dp_id, group_id, directory_basename, file_browse_path, file_basename) = (None,None,None,None,None,None,None,None,None)

try:
    with open('config.json') as json_file:
        data = json.load(json_file)
        base_url              = data['base_url']
        login                 = data['login']
        password              = data['password']
        file_copy_bourreau_id = data['file_copy_bourreau_id']
except:
    print("Error reading config.json file")
    exit()

credentials = {
    'login': login,
    'password': password
}

session_response = requests.post(
    url = '/'.join([base_url, 'session']),
    json = credentials,
    headers= { 'Accept': 'application/json' }
)

session_info = None

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

admin_token_params = (
    ('cbrain_api_token', session_info['cbrain_api_token']),
)


############################
# Get Bourreau information #
############################

print ('Getting Bourreau information...')
print ('Bourreau ID: ' + file_copy_bourreau_id)

bourreau_response = requests.get(
    url = '/'.join([base_url, 'bourreaux', file_copy_bourreau_id]),
    headers = api_headers,
    params = token_params
)

bourreau_info = None
if bourreau_response.status_code != requests.codes.ok:
    print('Failed to get Bourreau information.')
    exit()
else:
    print('Bourreau information retrieved.')
    bourreau_info = bourreau_response.json()
    print (json.dumps(bourreau_info, indent=2))

#################################
# Call users push keys method   #
#################################

print ('Pushing user SSH key with users_push_keys method...')
print ('User ID: ' + user_id)
print ('Bourreau IDs: ' + file_copy_bourreau_id)

push_keys_data = {
    'push_keys_to': [file_copy_bourreau_id]
}

push_keys_response = requests.put(
    url = '/'.join([base_url, 'users', str(user_id), 'push_keys']),
    headers = api_headers,
    params  = token_params,
    data    = json.dumps(push_keys_data)
)

print(push_keys_response.status_code)

if push_keys_response.status_code != requests.codes.ok:
    print('Failed to push user SSH key.')
    print ('Message: ' + push_keys_response.text)
    exit()
else:
    print('User SSH key pushed.')
    print ('Message: ' + push_keys_response.text)


