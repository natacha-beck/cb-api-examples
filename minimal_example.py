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
        s3_dp_id                         = data['s3_dp_id']
        uk_dp_id                         = data['uk_dp_id']
        group_id                         = data['group_id']
        directory_basename               = data['directory_basename']
        file_browse_path                 = data['file_browse_path']
        file_basename                    = data['file_basename']
        cloud_storage_client_identifier  = data['cloud_storage_client_identifier']
        cloud_storage_client_token       = data['cloud_storage_client_token']
        cloud_storage_client_bucket_name = data['cloud_storage_client_bucket_name']
        cloud_storage_client_path_start  = data['cloud_storage_client_path_start']
        cloud_storage_endpoint           = data['cloud_storage_endpoint']
        cloud_storage_region             = data['cloud_storage_region']
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

###############################
# 2. Browse S3 Data Providers #
###############################

print ("\n\n=== Browse Data Providers ===")

browse_dp_response = requests.get(
    url  = '/'.join([base_url, 'data_providers', s3_dp_id, 'browse']),
    headers = api_headers,
    params  = token_params,
)

if browse_dp_response.status_code != requests.codes.ok:
    print('DP browse failed.')
    failed_browse_dp_info = browse_dp_response.json()
    print(failed_browse_dp_info)
else:
    browse_dp_info = browse_dp_response.json()
    print("\nBrowse DP info:\n", browse_dp_info)

###########################################################
#                 3. Case of a directory                  #
#                                                         #
# a. Register the directory                               #
# b. Move the directory to an other DataProvider          #
# c. Download the file content via download               #
#                                                         #
###########################################################

print ("\n\n=== Work on Directory ===")

###########################
# a. Register a directory #
###########################

print ("\n\n=== Register a directory ===")

register_directory_data = {
    'basenames'  : [directory_basename],
    'filetypes'  : ['FileCollection-' + directory_basename],
}

register_directory_response = requests.post(
    url  = '/'.join([base_url, 'data_providers', s3_dp_id, 'register']),
    headers = api_headers,
    params  = token_params,
    data    = json.dumps(register_directory_data),
)

register_directory_info = None
if register_directory_response.status_code != requests.codes.ok:
    print('Directory registration failed.')
    failed_register_directory_info = register_directory_response.json()
    print(failed_register_directory_info)
else:
    print('Directory registration successful.')
    register_directory_info = register_directory_response.json()
    print("\nRegistered directory info:\n", register_directory_info)

##########################
# b. Copy a directory    #
##########################

print ("\n\n=== Copy the directory ===")

if register_directory_info != None:
    directory_id = register_directory_info['newly_registered_userfiles'][0]['id']

    change_provider_data = {
        'file_ids': [directory_id],
        'copy': "1",
        'data_provider_id_for_mv_cp': uk_dp_id,
    }

    change_provider_response = requests.post(
        url  = '/'.join([base_url, 'userfiles', 'change_provider']),
        headers = api_headers,
        params  = token_params,
        data    = json.dumps(change_provider_data),
    )

    if change_provider_response.status_code != requests.codes.ok:
        failed_change_provider_info = change_provider_response.json()
        print('Directory Copy failed:')
        print(failed_change_provider_info)
    else:
        change_provider_info = change_provider_response.json()
        print("\nCopied directory info:\n", change_provider_info)

############################
# c. Download a directory  #
# via userfiles/download   #
############################

print ("\n\n=== DL the directory via userfiles/download ===")

download_file_data = {
    'file_ids': [directory_id],
}

download_userfiles_response = requests.post(
    url  = '/'.join([base_url, 'userfiles', 'download']),
    headers  = api_headers,
    params   = token_params,
    data     = json.dumps(download_file_data),
)

if download_userfiles_response.status_code != requests.codes.ok:
    print('File download failed.')
else:
    file_name = directory_basename + '.tar.gz'
    open(file_name, 'wb').write(download_userfiles_response.content)
    print('File download successful. Under:', file_name)

###########################################################
#                4. Case of a file                        #
#                                                         #
# a. Register the file                                    #
# b. Copy the file to an other DataProvider (WIP)         #
# c. Download the file content via download               #
#                                                         #
###########################################################

print ("\n\n=== Work on a File ===")

###########################
# a. Register a file      #
###########################

print("\n\n=== Register a file ===")

register_file_data = {
    'basenames'  : [file_basename],
    'filetypes'  : ['ImageFile-' + file_basename],
    'browse_path': file_browse_path,
    'id'         : s3_dp_id,
}

register_file_response = requests.post(
    url  = '/'.join([base_url, 'data_providers', s3_dp_id, 'register']),
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

##########################
# b. Copy a file         #
##########################

# print ("\n\n=== TODO: Move the file === ISSUE ??? link to CBRAIN ===")
# print ("\n\n=== Due to the S3MultiLevelDataProvider ===")

# if register_file_info != None:
#     file_info = register_file_info['newly_registered_userfiles'][0]
#     print(file_info)
#     file_id   = str(file_info['id'])
#     file_name = file_info['name']

#     move_file_data = {
#         'file_ids': [file_id],
#         'data_provider_id_for_mv_cp': destination_dp_id,
#     }

#     move_file_response = requests.post(
#         url  = '/'.join([base_url, 'userfiles', 'change_provider']),
#         headers = api_headers,
#         params  = token_params,
#         data    = json.dumps(move_file_data),
#     )

#     if move_file_response.status_code != requests.codes.ok:
#         print('File move failed.')
#         failed_move_file_info = move_file_response.json()
#         print(failed_move_file_info)
#     else:
#         print('File move successful.')
#         move_file_info = move_file_response.json()
#         print("\n---Moved file info---\n", move_file_info)

##########################
# c. Download a file     #
# via userfiles/download #
##########################

print ("\n\n=== Download the file via userfiles/download ===")

if register_file_info != None:
    file_info = register_file_info['newly_registered_userfiles'][0]
    file_id   = str(file_info['id'])
    file_name = file_info['name']

    file_dl_info = {
        'file_ids': [file_id],
    }

    download_userfiles_response = requests.post(
        url  = '/'.join([base_url, 'userfiles', 'download']),
        headers  = api_headers,
        params   = token_params,
        data     = json.dumps(file_dl_info),
    )

    if download_userfiles_response.status_code != requests.codes.ok:
        print('File download failed.')
    else:
        print('File download successful.')
        open(file_name, 'wb').write(download_userfiles_response.content)

