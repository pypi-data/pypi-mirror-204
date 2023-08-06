import os,urllib3,json,sys,requests
import icpd_core
from icpd_core.api.access_management_api import AccessManagementApi
from icpd_core.api.service_instance_manager_v3_api import ServiceInstanceManagerV3Api
from icpd_core.api.connections_api import ConnectionsApi

api_client = None
amapi = None
smapi = None
conn_api = None

icpd_token = ''
zencoreapi_host = None

# Using environment var RUNTIME_ENV_APSX_URL published by Jupyter environment extract controlplane namespace
# after first period (.)
def extract_controlplane_ns():
    cplane_ns = None
    ns_delimiter = '.'
    # Getting internal ngix URL
    int_nginx_url = os.environ.get('RUNTIME_ENV_APSX_URL')
    if int_nginx_url is None:
        return
    fIndex = int_nginx_url.find(ns_delimiter)+1
    if fIndex <= 0:
        return
    nIndex = int_nginx_url[fIndex:].find(ns_delimiter)
    if nIndex <= 0:
        return
    cplane_ns = int_nginx_url[fIndex:fIndex+nIndex]
    return cplane_ns


def init_utils(host=None, token=None, verify_ssl=False):
    global api_client
    global amapi
    global smapi
    global conn_api
    global icpd_token
    global zencoreapi_host

    # Update after v2/secrets are exposed through internal nginx configuration
    cp_ns = extract_controlplane_ns()
    if cp_ns is None:
        zencoreapi_host = 'https://zen-core-api-svc:4444'
    else:
        zencoreapi_host = 'https://zen-core-api-svc.' + cp_ns + '.svc:4444'

    configuration = icpd_core.Configuration()

    configuration.host = host
    if host is None:
        configuration.host = 'https://zen-core-api-svc:4444'

    if token is None:
        token = os.environ.get('USER_ACCESS_TOKEN')

    authorization_token = 'Bearer ' + token
    configuration.verify_ssl = verify_ssl

    if not verify_ssl:
        urllib3.disable_warnings()

    if os.environ.get("ENV") == "development" and host is None:
        configuration.host = 'http://127.0.0.1:3333'

    # Set globals
    icpd_token = token
    api_client = icpd_core.ApiClient(configuration=configuration,header_name='Authorization', header_value=authorization_token)
    amapi = AccessManagementApi(api_client=api_client, )
    smapi = ServiceInstanceManagerV3Api(api_client=api_client)
    conn_api = ConnectionsApi(api_client=api_client)

def get_instance_token(name='', instance_type='', instance_id=''):
    try:
        if instance_id != '':
            body_param = { "serviceInstanceID": instance_id}
            resp = amapi.generate_token(body_param)
        elif instance_type != '' and name != '':
            body_param= { "serviceInstanceDisplayName": name, "serviceInstanceType": instance_type}
            resp = amapi.generate_token(body_param)
        elif name != '':
            body_param = { "serviceInstanceDisplayName": name}
            resp = amapi.generate_token(body_param)
        else:
            sys.exit('ERROR: Provide name and instance_type OR instance_id to get the instance token')
    except (SystemExit) as e:
        raise
    except (ibm_cpd_core.rest.ApiException) as e:
        if e.body and is_json_valid(e.body):
            json_object = json.loads(e.body)
            if '_statusCode_' in json_object and json_object["_statusCode_"] == 409:
                print('ERROR: Multiple instances with the same name exist. Provide name and instance_type OR instance_id as input arguments.')
                raise
            elif 'exception' in json_object:
                raise Exception(e.status, json_object["exception"])
            elif 'message' in json_object:
                raise Exception(e.status, json_object["message"])
            else:
                raise Exception(e.status)
        else:
            raise Exception(e.status)

    return resp.access_token

def get_connection_info(name='', instance_id=''):
    if name != '':
        try:
            result = smapi.get_service_instance_v3(display_name = name)
        except ibm_cpd_core.rest.ApiException:
            result = smapi.get_service_instance_v3(s_id = instance_id)
    elif instance_id != '':
        result = smapi.get_service_instance_v3(s_id = instance_id)

    return result

def get_connection(name, conn_class='external'):
    """Get connection details by the connection name

    Args:
      name (string): Connection name.
      conn_class (string) optional: Connection class. Either "external" or "svc" (default "external")

    Returns:
    dict: Connection details

    Raises:
      Exception: (status, message)

    """

    try:
        # Get the connection details by providing the name and optionally the class
        api_response = conn_api.get_connection_v3(name, _class=conn_class)
    except ibm_cpd_core.rest.ApiException as e:
        if is_json_valid(e.body):
            json_obj = json.loads(e.body)
            if 'exception' in json_obj:
                raise Exception(e.status, json_obj["exception"])
            elif 'message' in json_obj:
                raise Exception(e.status, json_obj["message"])
            else:
                raise Exception(e.status)
        else:
            raise Exception(e.status)

    return api_response.connection

def get_connections(conn_class='all'):
    """Get list of all connections and optionally filter by class name

    Args:
      conn_class (string) optional: Connection class. Either "external" or "svc" (default "external")

    Returns:
      []dict: List of connections

    Raises:
      Exception: (status, message)

    """

    try:
        # Get the list of connections.
        api_response = conn_api.get_connections_v3(_class=conn_class)
    except ibm_cpd_core.rest.ApiException as e:
        if is_json_valid(e.body):
            json_obj = json.loads(e.body)
            if 'exception' in json_obj:
                raise Exception(e.status, json_obj["exception"])
            elif 'message' in json_obj:
                raise Exception(e.status, json_obj["message"])
            else:
                raise Exception(e.status)
        else:
            raise Exception(e.status)

    return api_response.connections

def get_service_instance_details(name='', instance_type='', instance_id=''):
    global icpd_token

    config = {}
    config['user_token'] = icpd_token
    config['service_token'] = get_instance_token(name = name, instance_type=instance_type, instance_id=instance_id)
    result = get_connection_info(name = name, instance_id=instance_id)
    config['connection_info'] = result.request_obj['CreateArguments']['connection-info']
    config['type'] = result.request_obj['ServiceInstanceType']

    return config

def _extract_error_message(err_resp, default_message):
   if default_message == '':
      default_message = 'Internal error: No default error message is defined'
   if not err_resp:
      raise Exception('err_resp (first) parameter is required')
   else:      
      try:
         msg = json.loads(err_resp)
         errMsg = msg['errors'][0]['message']
      except ValueError:
         errMsg = default_message

   return errMsg 

def _fetch_my_secrets_v2(resp):
    secrets = list(resp['secrets'])
    limit = 50
    if resp['total_count'] > limit:
        offset = 50
        while offset < resp['total_count']:
            url = _get_zencoreapi_host() + '/v2/secrets?sort=-created_at&offset='+str(offset)+'&limit='+str(limit)
            headers = {
                'Authorization': 'Bearer ' + icpd_token
            }

            r = requests.get(url, headers=headers)

            if r.status_code != 200:
                defaultMsg = "non 200 error response"
                errMsg = _extract_error_message(r.text, defaultMsg)
                raise Exception("Received error  for offset {} status code: {} message: {}".format(index, r.status_code, errMsg))
            else:
                try:
                    resp = r.json()

                    if resp['secrets']:
                        secrets.extend(list(resp['secrets']))
                    else:
                        raise Exception('Internal error: Something is not right, secret data is not available for offset {}'.format(index))
                except Exception:
                    raise Exception('secrets could not be retrieved for offset {}'.format(index))
            offset+=limit
    return secrets

# set_zencoreapi_host allows overwriting zencoreapi host
# To access from dataplane namespace set it to https://zen-core-api-svc.<controlplane-ns>.svc:4444
def set_zencoreapi_host(host):
    global zencoreapi_host 
    zencoreapi_host = host
    if not host:
        zencoreapi_host = 'https://zen-core-api-svc:4444'

# _get_zencoreapi_host returns zencoreapi host
def _get_zencoreapi_host():
    global zencoreapi_host     
    return zencoreapi_host

# get_my_secrets_v2 returns secret list available to user
# first get 50 secrets by calling v2/secrets API
# if more than secrets are available then delegate to method _fetch_my_secrets_v2 
def get_my_secrets_v2():
    global icpd_token

    limit = 50
    url = _get_zencoreapi_host() + '/v2/secrets?sort=-created_at&offset=0&limit='+str(limit)
    headers = {
        'Authorization': 'Bearer ' + icpd_token
    }

    r = requests.get(url, headers=headers)

    if r.status_code == 401:
        raise Exception('User not authorized to access secrets')
    elif r.status_code != 200:
        defaultMsg = "non 200 error response"
        errMsg = _extract_error_message(r.text, defaultMsg)
        raise Exception("Received error status code: {} message: {}".format(r.status_code, errMsg))
    else:
        try:
            resp = r.json()

            if resp['secrets']:
                secrets = _fetch_my_secrets_v2(resp)
                return secrets

            else:
                raise Exception('Internal error: Something is not right, unable to parse secret data')
        except Exception:
            raise Exception('Internal error: Something is not right, unable to parse secret data')

    return None

# get_my_secret_details_v2 takes secret_urn as parameter and returns
# secret details by calling v2/secrets/{secret-urn} API
def get_my_secret_details_v2(secret_urn):
    if not secret_urn:
        raise Exception('secret_urn parameter is required')
    else:
        global icpd_token

        url = _get_zencoreapi_host() + '/v2/secrets/' + secret_urn
        headers = {
            'Authorization': 'Bearer ' + icpd_token
        }

        r = requests.get(url, headers=headers)
        print("Response.json {}".format(r))
        if r.status_code == 401:
            raise Exception('User not authorized to access secrets')
        elif r.status_code != 200:
            defaultMsg = "non 200 error response"
            errMsg = _extract_error_message(r.text, defaultMsg)
            raise Exception("Received error status code: {} message: {}".format(r.status_code, errMsg))
        else:
            try:
                resp = r.json()

                if resp['data']:
                    return resp
                else:
                    raise Exception('Internal error: Something is not right, secret data is not available')
            except Exception:
                raise Exception('Internal error: Something is not right, unable to parse secret data')

        return None

init_utils()

def is_json_valid(json_obj):
    try:
        json_object = json.loads(json_obj)
    except ValueError:
        return False

    return True
