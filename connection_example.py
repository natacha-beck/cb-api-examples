import requests
import json
import getpass

# Extract information from ./config.json
(base_url, login, password, s3_dp_id, uk_dp_id, user_uk_dp_id, group_id, directory_basename, file_browse_path, file_basename, user_id) = (None,None,None,None,None,None,None,None,None,None,None)

# Read JSON file ./config.json
try:
    with open('./config.json') as json_file:
        data = json.load(json_file)
        print('\n------Configuration data------')
        print(data,"\n")
        base_url                         = data['base_url']
        login                            = data['login']
        password                         = data['password']
        s3_dp_id                         = data['s3_dp_id']
        uk_dp_id                         = data['uk_dp_id']
        group_id                         = data['group_id']
        directory_basename               = data['directory_basename']
        directory_file_basename          = data['directory_file_basename']
        file_browse_path                 = data['file_browse_path']
        file_basename                    = data['file_basename']
        user_id                          = data['user_id']
        user_uk_dp_id                    = data['user_uk_dp_id']
except:
    print("Error reading ./config.json")
    exit()

#####################
# 1. login as admin #
#####################

print('\n------Login as admin------')

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
    print('Login as admin failed.')
    exit()
else:
    session_info = session_response.json()
    print('Login successful.')
    print("******Admin session info:\n", session_info)

api_headers = {
    'Content-Type': 'application/json',
    'Accept'      : 'application/json',
}

admin_token_params = (
    ('cbrain_api_token', session_info['cbrain_api_token']),
)

####################################################
# 2. Browse S3 (accessible by admin only) as admin #
####################################################

print('\n------S3 Data Provider Browse as admin (accessible)------')

# Browse the S3 data provider as admin
s3_dp_browse_as_admin_response = requests.get(
    url = '/'.join([base_url, 'data_providers', s3_dp_id, 'browse']),
    headers = api_headers,
    params = admin_token_params
)

if s3_dp_browse_as_admin_response.status_code != requests.codes.ok:
    print('S3 browse as admin failed.')
    exit()
else:
    print("******S3 browse as admin successful:")
    print(s3_dp_browse_as_admin_response.json())

######################################
# 3. Browse UK as admin (accessible) #
######################################

print('\n------UK Data Provider Browse as admin user (accessible)------')

# Browse the personal data provider
uk_dp_browse_as_admin_response = requests.get(
    url = '/'.join([base_url, 'data_providers', user_uk_dp_id, 'browse']),
    headers = api_headers,
    params  = admin_token_params
)

if uk_dp_browse_as_admin_response.status_code != requests.codes.ok:
    print('UK browse as admin failed.')
    exit()
else:
    print("******UK browse as admin successful:")
    print(uk_dp_browse_as_admin_response.json())

#######################################
# 4. Create session for standard user #
#######################################

print('\n------Create session for standard user------')

create_user_session = requests.post(
    url = '/'.join([base_url, 'users', user_id, 'create_user_session']),
    headers = api_headers,
    params  = admin_token_params
)

user_cbrain_api_token = None
if create_user_session.status_code != requests.codes.ok:
    print('Create session for standard user failed.')
    exit()
else:
    print("******Create session for standard user successful:")
    print(create_user_session.json())
    user_cbrain_api_token = create_user_session.json()['cbrain_api_token']

user_token_params = (
    ('cbrain_api_token', user_cbrain_api_token),
)

######################################################
# 5. Browse S3 DataProvider as user (not accessible) #
######################################################

print('\n------S3 Data Provider Browse as standard user (not accessible)------')

# Browse the S3 data provider
s3_dp_browse_as_user_response = requests.get(
    url = '/'.join([base_url, 'data_providers', s3_dp_id, 'browse']),
    headers = api_headers,
    params  = user_token_params
)

if s3_dp_browse_as_user_response.status_code != requests.codes.ok:
    print('S3 browse as user failed.')
else:
    print("******S3 browse as user successful:")
    print(s3_dp_browse_as_user_response.json())

#############################################
# 6. Browse UK as user (accessible by user) #
#############################################

print('\n------UK Data Provider Browse as standard user (accessible)------')

uk_dp_browse_as_user_response = requests.get(
    url = '/'.join([base_url, 'data_providers', user_uk_dp_id, 'browse']),
    headers = api_headers,
    params  = user_token_params
)

if uk_dp_browse_as_user_response.status_code != requests.codes.ok:
    print('UK browse as user failed.')
else:
    print("******UK browse as user successful:")
    print(uk_dp_browse_as_user_response.json())
