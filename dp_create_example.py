import requests
import json
import getpass

# Extract information from ./config.json
(base_url, login, password, s3_dp_id, uk_dp_id, group_id, directory_basename, file_browse_path, file_basename, uk_dp_name, uk_dp_remote_host, uk_dp_remote_user, uk_dp_remote_dir, uk_dp_remote_dir) = (None,None,None,None,None,None,None,None,None,None,None,None,None,None)

# Read JSON file ./config.json
try:
    with open('./config.json') as json_file:
        data = json.load(json_file)
        print(data)
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
        uk_dp_name                       = data['uk_dp_name']
        uk_dp_remote_host                = data['uk_dp_remote_host']
        uk_dp_remote_user                = data['uk_dp_remote_user']
        uk_dp_remote_dir                 = data['uk_dp_remote_dir']
        uk_dp_group_id                   = data['uk_dp_group_id']
        cloud_storage_client_identifier  = data['cloud_storage_client_identifier']
        cloud_storage_client_token       = data['cloud_storage_client_token']
        cloud_storage_client_bucket_name = data['cloud_storage_client_bucket_name']
        cloud_storage_client_path_start  = data['cloud_storage_client_path_start']
        cloud_storage_endpoint           = data['cloud_storage_endpoint']
        cloud_storage_region             = data['cloud_storage_region']
        s3_name                          = data['s3_name']

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

#############################################
# 2. Create a UserkeyFlatDirSshDataProvider #
#############################################

print("=== Create a UserkeyFlatDirSshDataProvider ===")

ssh_dp_info = {
    'data_provider': {
        'name': uk_dp_name,
        'remote_host': uk_dp_remote_host,
        'remote_user': uk_dp_remote_user,
        'remote_dir': uk_dp_remote_dir,
        'cloud_storage_client_token': "remote_storage_client_token"
    }
}

create_ssh_dp_response = requests.post(
    url  = '/'.join([base_url, 'data_providers', 'create_personal']),
    headers = api_headers,
    params  = token_params,
    data    = json.dumps(ssh_dp_info),
)

create_ssh_dp_info = None
if create_ssh_dp_response.status_code != requests.codes.ok:
    print('DP creation failed.')
    failed_ssh_dp_info = create_ssh_dp_response.json()
    print(failed_ssh_dp_info)
    exit()
else:
    print('DP creation successful.')
    create_ssh_dp_info = create_ssh_dp_response.json()
    print(create_ssh_dp_info)

######################################
# 3. Check_personal to put it online #
######################################

print("=== Check_personal to put it online ===")

check_ssh_dp_response = requests.post(
    url  = '/'.join([base_url, 'data_providers', str(create_ssh_dp_info['id']), 'check_personal']),
    headers = api_headers,
    params  = token_params,
)

if check_ssh_dp_response.status_code != requests.codes.ok:
    print('DP check failed.')
else:
    print('DP check successful.')

######################################
# 4. Get DP info                     #
######################################

print("=== Get DP info ===")

get_ssh_dp_response = requests.get(
    url  = '/'.join([base_url, 'data_providers', str(create_ssh_dp_info['id'])]),
    headers = api_headers,
    params  = token_params,
)

if get_ssh_dp_response.status_code != requests.codes.ok:
    print('DP get failed.')
else:
    print('DP get successful.')
    print(get_ssh_dp_response.json())

#########################################
# 5. Create a S3MultiLevelDataProvider #
########################################

print ("=== Create a S3MultiLevelDataProvider ===")

s3_dp_info = {
    'data_provider': {
        'type': "S3MultiLevelDataProvider",
        'name': s3_name,
        'cloud_storage_client_identifier': cloud_storage_client_identifier,
        'cloud_storage_client_token': cloud_storage_client_token,
        'cloud_storage_client_bucket_name': cloud_storage_client_bucket_name,
        'cloud_storage_client_path_start': cloud_storage_client_path_start,
        'cloud_storage_endpoint': cloud_storage_endpoint,
        'cloud_storage_region': cloud_storage_region
    }
}

create_s3multi_dp_response = requests.post(
    url  = '/'.join([base_url, 'data_providers', 'create_personal']),
    headers = api_headers,
    params  = token_params,
    data    = json.dumps(s3_dp_info),
)

if create_s3multi_dp_response.status_code != requests.codes.ok:
    print('DP creation failed.')
    failed_s3multi_dp_info = create_s3multi_dp_response.json()
    print(failed_s3multi_dp_info)
else:
    print('DP creation successful.')
    create_s3multi_dp_info = create_s3multi_dp_response.json()
    print(create_s3multi_dp_info)

######################################
# 6. Check_personal to put it online #
######################################

print("=== Check_personal to put it online ===")

check_s3multi_dp_response = requests.post(
    url  = '/'.join([base_url, 'data_providers', str(create_s3multi_dp_info['id']), 'check_personal']),
    headers = api_headers,
    params  = token_params,
)

if check_s3multi_dp_response.status_code != requests.codes.ok:
    print('DP check failed.')
else:
    print('DP check successful.')

######################################
# 7. Get DP info                     #
######################################

print("=== Get DP info ===")

get_s3multi_dp_response = requests.get(
    url  = '/'.join([base_url, 'data_providers', str(create_s3multi_dp_info['id'])]),
    headers = api_headers,
    params  = token_params,
)

if get_s3multi_dp_response.status_code != requests.codes.ok:
    print('DP get failed.')
else:
    print('DP get successful.')
    print(get_s3multi_dp_response.json())
