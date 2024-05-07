import requests
import json

# Extract information from ./config.json
# (base_url, login, password, s3_dp_id, uk_dp_id, group_id, directory_basename, file_browse_path, file_basename, uk_dp_name, uk_dp_remote_host, uk_dp_remote_user, uk_dp_remote_dir, uk_dp_remote_dir) = (None,None,None,None,None,None,None,None,None,None,None,None,None,None)
(base_url, login, password, orig_dp_id, dest_dp_id) = (None,None,None,None,None)

# Read JSON file ./config.json
try:
    with open('./config.json') as json_file:
        data = json.load(json_file)
        base_url                         = data['base_url']
        login                            = data['login']
        password                         = data['password']
        orig_dp_id                       = data['orig_dp_id']
        dest_dp_id                       = data['dest_dp_id']
        file_basename_json               = data['file_basename_json']

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

# Create a session as admin
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

###############################################
# 1. Register file from SSH Data Provider     #
###############################################

# Register a file from SSH Data Provider 1

print("\n\n=== Register a file ===")

register_file_data = {
    'basenames'  : [file_basename_json],
    'filetypes'  : ['JsonFile-' + file_basename_json],
    'id'         : orig_dp_id
}

register_file_response = requests.post(
    url  = '/'.join([base_url, 'data_providers', orig_dp_id, 'register']),
    headers = api_headers,
    params  = token_params,
    data    = json.dumps(register_file_data),
)

register_file_info = None

if register_file_response.status_code != requests.codes.ok:
    failed_register_file_info = register_file_response.json()
    print('File registration failed.')
    print(failed_register_file_info)
else:
    register_file_info = register_file_response.json()
    print('File registration successful.')
    print("\nRegistered file info\n", register_file_info)

#################################
# Extract id of registered file #
#################################

file_id = None

if register_file_info != None:
    file_info = register_file_info['newly_registered_userfiles'][0]
    print(file_info)
    file_id   = str(file_info['id'])

    print("\n\n=== File ID ===")
    print(file_id)

###############################################
# 2. Copy file from SSH Data Provider 1 to 2  #
#            without using cache              #
#           using dispatcher_file_copy        #
###############################################

print("\n\n=== Copy file from SSH Data Provider 1 to 2 without using cache ===")

dispatcher_file_copy_data = {
    'data_provider_id'  : dest_dp_id,
    'userfile_ids'      : [file_id],
    'bypass_cache'      : 'yes'
}

dispatcher_file_copy_response = requests.post(
    url  = '/'.join([base_url, 'bourreaux', 'dispatcher_file_copy']),
    headers = api_headers,
    params  = token_params,
    data    = json.dumps(dispatcher_file_copy_data),
)

print ("\n\n=== Dispatcher File Copy Response ===")
print(dispatcher_file_copy_response)

if dispatcher_file_copy_response.status_code != requests.codes.ok:
    failed_dispatcher_file_copy_data = dispatcher_file_copy_response.json()
    print('Directory Copy failed:')
    print(failed_dispatcher_file_copy_data)
else:
    dispatcher_file_copy_data_info = dispatcher_file_copy_response.json()
    print("\nCopied directory info:\n", dispatcher_file_copy_data_info)

