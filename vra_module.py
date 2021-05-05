"""
vRealize Automation 8.x Module for Salt
========================================

Provides methods to configure and setup vRealize Automation

Requirements:
SaltStack Config
vRealize Automation 8.x

"""


#Import python libs
import logging
try:
    import json
    import requests
    import urllib3
    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False

log = logging.getLogger(__name__)

__virtual_name__ = 'vra'

def __virtual__():
    '''
    Only load vra if requests is available
    '''
    if HAS_DEPENDENCIES:
        return __virtual_name__
    else:
        return False, 'The vra module cannot be loaded: dependency packages unavailable.'

urllib3.disable_warnings()

def set_bas_url(url):
    api_url_base = "https://" + url + "/"
    return api_url_base

def extract_values(obj, key):
    """
    Pull all values of specified key from nested JSON.
    """
    arr = []
    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr
    results = extract(obj, arr, key)
    return results

def get_token(url,username,password):
    """
    Retrieve Session Token from vRealize Automation

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password
    """
    api_url_base = set_bas_url(url)
    headers = {'Content-Type': 'application/json'}
    api_url = '{0}csp/gateway/am/api/login'.format(api_url_base)
    data =  {
              "username": username,
              "password": password
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        key = json_data['cspAuthToken']
        return key
    else:
        return response.status_code

##########Cloud Assembly Configuration Functions##########

######Cloud Account and Cloud Zones######
def create_aws_ca(url,username,password,aws_key_id,aws_access_key,name,region_name,create_zone="false"):
    """
    Setup and configure AWS Cloud Accounts

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    aws_key_id = AWS Key

    aws_access_key = AWS Access Key

    name = Name of AWS Integration

    region_name = Name of the region to assign (i.e us-west-1 or 'us-west-1,us-west-2' for multiple regions)

    create_zone = Should vRA create a Cloud Zone for each region (default is true)

    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/cloud-accounts-aws'.format(api_url_base)
    region_array = region_name.split(',')
    data =  {
                "description": "AWS Cloud Account",
                "accessKeyId": aws_key_id,
                "secretAccessKey": aws_access_key,
                "cloudAccountProperties": {

                },
                "regionIds": region_array,
                "createDefaultZones" : create_zone,
                "name": name
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        print('Successfully Created AWS Cloud Account')
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_azure_ca(url,username,password,sub_id,ten_id,app_id,app_key,name,region_name,create_zone="false"):
    """
    Setup and Create Azure Cloud Account

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    sub_id = Azure Subscription ID

    ten_id = Azure Tenant ID

    app_id = Azure Client Application ID

    app_key = Azure Client Application Secret Key

    region_name = Azure Region (example: eastus or 'eastus,westus' for multiple regions)

    create_zone = Should vRA create a Cloud Zone for each region (default is true)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/cloud-accounts-azure'.format(api_url_base)
    region_array = region_name.split(',')
    data =  {
              "name": name,
              "description": "Azure Cloud Account",
              "subscriptionId": sub_id,
              "tenantId": ten_id,
              "clientApplicationId": app_id,
              "clientApplicationSecretKey": app_key,
              "regionIds": region_array,
              "createDefaultZones": create_zone
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        print('Successfully Created Azure Cloud Account')
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_vsphere_ca(url,username,password,vc_hostname,vc_username,vc_password,name,region_name,create_zone="false"):
    """
    Setup and Create vSphere Cloud Account

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    vc_hostname = vCenter IP / FQDN

    vc_username: vCenter Administrator User

    vc_password = vCenter Password

    name = Cloud Account Name

    region_name = vCenter Datacenter (i.e. Datacenter:datacenter-2 or 'Datacenter:datacenter-1,Datacenter:datacenter-2' for multiple regions)

    create_zone = Should vRA create a Cloud Zone for each region (default is true)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/cloud-accounts-vsphere'.format(api_url_base)
    region_array = region_name.split(',')
    data = {
              "name": name,
              "hostName": vc_hostname,
              "acceptSelfSignedCertificate": "true",
              "dcid": "onprem",
              "username": vc_username,
              "password": vc_password,
              "regionIds": region_array,
              "createDefaultZones": create_zone
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        print('Successfully Created vCenter Cloud Account')
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_ca_by_name(url,username,password,caname):
    """
    Retrieve Cloud Account by its names for further configurations

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    ca_name = Cloud Account Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/cloud-accounts'.format(api_url_base)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            ca_name = json_data['content'][n]['name']
            if ca_name == caname:
                print("Found Cloud Account: " + caname)
                ca_json = json_data['content'][n]
                return ca_json
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For Cloud Zone: " + caname)
                return "No Match Found For Cloud Zone: " + caname
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_nsxt_ca(url,username,password,nsx_hostname,nsx_username,nsx_password,name,ca_name):
    """
    Create NSX Cloud Account

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    nsx_hostname = FQDN of NSX Manager Instance

    nsx_username = NSX Admin User

    nsx_password = NSX Admin Password

    name = Provide a name for the Cloud Account

    ca_name = Name of Cloud Account to associate with NSX Cloud Account
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    ca_json = get_ca_by_name(url,username,password,ca_name)
    ca_id = ca_json['id']
    ca_array = []
    ca_array.append(ca_id)
    api_url = '{0}iaas/api/cloud-accounts-nsx-t'.format(api_url_base)
    data = {
              "hostName": nsx_hostname,
              "acceptSelfSignedCertificate": "true",
              "password": nsx_password,
              "dcid": "onprem",
              "associatedCloudAccountIds": ca_array,
              "managerMode": "true",
              "name": name,
              "description": "NSX-T Cloud Account",
              "username": nsx_username
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        print('Successfully Created NSX-T Cloud Account')
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_czid_by_name(url,username,password,czname):
    """
    Retrieve Cloud Zone by Name for further configurations

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    czname = Cloud Zone Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/zones'.format(api_url_base,czname)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            cz_name = json_data['content'][n]['name']
            if cz_name == czname:
                print("Found Cloud Zone: " + czname)
                cz_id = json_data['content'][n]['id']
                return cz_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For Cloud Zone: " + czname)
                return "No Match Found For Cloud Zone: " + czname
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_region_by_caname(url,username,password,region_name,caname):
    """
    Retrieve Region ID that is=assocaited to a specific Cloud Account

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    region_name = region_name = Region inside of vRA (e.g. - us-west-1, Datacenter:datacenter-2)

    czaname = Cloud Account Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/regions'.format(api_url_base)
    response = requests.get(api_url, headers=headers, verify=False)
    ca_json = get_ca_by_name(url,username,password,caname)
    ca_id = ca_json['id']
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            reg_name = json_data['content'][n]['name']
            if reg_name == region_name:
                print("Found Region: " + region_name)
                caid = json_data['content'][n]['_links']['cloud-account']['href']
                caid = caid[25:]
                if caid == ca_id:
                    reg_id = json_data['content'][n]['id']
                    return reg_id
                    break
                elif n < end_n:
                    n = n + 1
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For Region: " + region_name)
                return "No Match Found For Region: " + region_name
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_cloudzone(url,username,password,czname,region_name,caname,folder=None,ppolicy="DEFAULT"):
    """
    Create Cloud Zone

    Arguments:

    url = vRA FQDN

    username = vRA Admin

    password = vRA Admin Password

    czname = Provide a name for the Cloud Zone

    region_name = Region inside of vRA (e.g. - us-west-1, Datacenter:datacenter-2)

    caname = Cloud Zone Name

    ppolicy = Placement Policy. Options are DEFAULT, BINPACK, SPREAD (DEFAULT is the default)

    folder = vSphere Folder Name (i.e. dev_vms)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    reg_id = get_cloud_regionid_by_name(url,username,password,region_name)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/zones'.format(api_url_base)
    if folder != None:
        data =  {
                    "name": czname,
                    "desc": czname + " Cloud Zone",
                    "regionId": reg_id,
                    "placementPolicy": ppolicy,
                    "advancedPlacementPolicyFailureToggle":"false",
                    "customProperties":{
                              "resourceGroupName": folder
                    }
                }
    else:
        data =  {
                    "name": czname,
                    "desc": czname + " Cloud Zone",
                    "regionId": reg_id,
                    "placementPolicy": ppolicy,
                    "advancedPlacementPolicyFailureToggle":"false",
                }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        json_data = json.loads(response.content.decode('utf-8'))
        print('Successfully Created Cloud Zone')
        return json_data['id']
    else:
        print(response.status_code)
        print(response.text)
        return response.status_code

def tag_cloudzone(url,username,password,czname,tag_key,tag_value):
    """
    Tag Cloud Zone

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    czname = Cloud Zone Name

    tag_key = Key for the tag (i.e. env:tag_value)

    tag_value = Value for the tag (i.e. tag_key:vsphere)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    czid = get_czid_by_name(url,username,password,czname)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/zones/{1}'.format(api_url_base,czid)
    data =  {
              "name": czname,
              "tags": [
                {
                  "key": tag_key,
                  "value": tag_value
                }
              ]
            }
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print('Successfully Tagged Cloud Zone')
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def delete_cloudzone(url,username,password,czname):
    """
    Delete Cloud Zone

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    czname = Cloud Zone Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    czid = get_czid_by_name(url,username,password,czname)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/zones/{1}'.format(api_url_base,czid)
    response = requests.delete(api_url, headers=headers, verify=False)
    if response.status_code == 204:
        print('Successfully Deleted Cloud Zone: ' + czname)
        return 'Successfully Deleted Cloud Zone: ' + czname
    else:
        print(response.status_code)
        return response.status_code

def delete_cloudaccount(url,username,password,ca_name):
    """
    Delete Cloud Account

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    ca_name = Cloud Account Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    ca_json = get_ca_by_name(url,username,password,czname)
    ca_id = ca_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/zones/{1}'.format(api_url_base,ca_id)
    response = requests.delete(api_url, headers=headers, verify=False)
    if response.status_code == 204:
        print('Successfully Deleted Cloud Account: ' + czname)
        return 'Successfully Deleted Cloud Account: ' + czname
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

######Projects######
def create_project(url,username,password,name):
    """
    Create a Project

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    name = Name of the Project
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/projects'.format(api_url_base)
    data =  {
              "administrators": [],
              "members": [],
              "operationTimeout": 0,
              "sharedResources": "true",
              "name": name,
              "description": "Project for " + name
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        json_data = json.loads(response.content.decode('utf-8'))
        print('Successfully Created Project')
        return json_data['id']
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_proj_by_name(url,username,password,projname):
    """
    Get Project by Name

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    projname: Name of the Project to search for
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/projects'.format(api_url_base,projname)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            proj_name = json_data['content'][n]['name']
            if proj_name == projname:
                print("Found Project: " + projname)
                proj_id = json_data['content'][n]
                return proj_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For Project: " + projname)
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def add_member_to_project(url,username,password,projname,member_email):
    """
    Add a member to a Project

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    projname = Project you want to add the user to

    member_email = email of the user you want to add to the project
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    proj_json = get_proj_by_name(url,username,password,projname)
    proj_id = proj_json['id']
    proj_members = proj_json['members']
    member_len = (len(proj_members))
    new_member = {"email": member_email,"type": "user"}
    payload = []
    if member_len == 0:
        payload.append(new_member)
    else:
        n = 0
        end = member_len - 1
        while True:
            if n <= end:
                payload.append(proj_members[n])
                n = n + 1
            elif n > end:
                break
        payload.append(new_member)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/projects/{1}'.format(api_url_base,proj_id)
    data =  {
              "members": payload
            }
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print("Successfully added " + member_email + " to Project as member")
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def add_admin_to_project(url,username,password,projname,admin_email):
    """
    Add and admin to the Project

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    projname = Provide name of project you want to add Admin to

    admin_email: Email of the admin you want to add (admins can manage a project)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username,password)
    proj_json = get_proj_by_name(url,username,password,projname)
    proj_id = proj_json['id']
    proj_admins = proj_json['administrators']
    admin_len = (len(proj_admins))
    new_admin = {"email": admin_email,"type": "user"}
    payload = []
    if admin_len == 0:
        payload.append(new_admin)
    else:
        n = 0
        end = admin_len - 1
        while True:
            if n <= end:
                payload.append(proj_admins[n])
                n = n + 1
            elif n > end:
                break
        payload.append(new_admin)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/projects/{1}'.format(api_url_base,proj_id)
    data =  {
              "administrators": payload
            }
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print("Successfully added " + admin_email + " to Project as admin")
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def add_group_member_to_project(url,username,password,projname,group_email):
    """
    Add a group to a Project

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    projname = Provide name of project you want to add group members to

    group_email = Email of the group you want to add (e.g. - vRA-All-Services-Users@acme.local)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    proj_json = get_proj_by_name(url,username,password,projname)
    proj_id = proj_json['id']
    proj_members = proj_json['members']
    member_len = (len(proj_members))
    new_member = {"email": group_email,"type": "group"}
    payload = []
    if member_len == 0:
        payload.append(new_member)
    else:
        n = 0
        end = member_len - 1
        while True:
            if n <= end:
                payload.append(proj_members[n])
                n = n + 1
            elif n > end:
                break
        payload.append(new_member)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/projects/{1}'.format(api_url_base,proj_id)
    data =  {
              "members": payload
            }
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print("Successfully added " + group_email + " to Project as member")
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def add_group_admin_to_project(url,username,password,projname,group_email):
    """
    Add group admin to a Project

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    projname = Provide name of project to add the admin group

    group_email: Email of the group you want to add (i.e. - vRA-All-Services-admins@acme.local

    """


    api_url_base = set_bas_url(url)
    access_key = get_token(url,username,password)
    proj_json = get_proj_by_name(url,username,password,projname)
    proj_id = proj_json['id']
    proj_admins = proj_json['administrators']
    admin_len = (len(proj_admins))
    new_admin = {"email": group_email,"type": "group"}
    payload = []
    if admin_len == 0:
        payload.append(new_admin)
    else:
        n = 0
        end = admin_len - 1
        while True:
            if n <= end:
                payload.append(proj_admins[n])
                n = n + 1
            elif n > end:
                break
        payload.append(new_admin)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/projects/{1}'.format(api_url_base,proj_id)
    data =  {
              "administrators": payload
            }
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print("Successfully added " + group_email + " to Project as admin")
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def add_cloudzone_to_project(url,username,password,projname,czname,priority=None,store_limit=None,cpu_limit=None,mem_limit=None,max_num=None):
    """
    Add CloudZone to a Project, once the CloudZone is added that Project can then consume resources in that CloudZone
    via Cloud Templates and Code Stream Pipelines.

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    projname = Provide name of a project you want to add the CloudZone

    czname = Name of CloudZone to Add (e.g. - "AWS-Cloud-Account / us-west-1")

    priority = 0 is the highest

    store_limit = Max amount of storage that the cloud zone can consume in this project(default=0, vSphere Cloud Zone only)

    cpu_limit = Max number of virtual CPUs that the cloud zone can consume in this project(default=0, unlimited)

    mem_limit = Maximum amount of memory (MB) that the cloud zone can consume in this project(default=0, unlimited)

    max_num = Maximum amount of instances that the cloud zone can deploy in this project(default=0, unlimited)

    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username,password)
    proj_json = get_proj_by_name(url,username,password,projname)
    proj_id = proj_json['id']
    proj_zones = proj_json['zones']
    zone_len = (len(proj_zones))
    czid = get_czid_by_name(url,username,password,czname)
    if priority is None:
        priority = 0
    if store_limit is None:
        store_limit = 0
    if cpu_limit is None:
        cpu_limit = 0
    if mem_limit is None:
        mem_limit = 0
    if max_num is None:
        max_num = 0
    new_zone = {"storageLimitGB": store_limit,"cpuLimit": cpu_limit,"memoryLimitMB": mem_limit,"zoneId": czid,"maxNumberInstances": max_num,"priority": priority}
    payload = []
    if zone_len == 0:
        payload.append(new_zone)
    else:
        n = 0
        end = zone_len - 1
        while True:
            if n <= end:
                payload.append(proj_zones[n])
                n = n + 1
            elif n > end:
                break
        payload.append(new_zone)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/projects/{1}'.format(api_url_base,proj_id)
    data =  {
              "zoneAssignmentConfigurations": payload
            }
    print(data)
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print("Successfully added Cloud Zone " + czname + " to Project")
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def enable_tf_on_project(url,username,password,projname):
    """
    Enable Terraform Service on a Project

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    projname: Provide name of a Project to add the Terraform service
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    proj_json = get_proj_by_name(url,username,password,projname)
    proj_id = proj_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}project-service/api/projects/{1}'.format(api_url_base,proj_id)
    data =  {
              "properties": {
                 "__allowTerraformCloudzoneMapping": "true"
              }
            }
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print("Successfully enabled Terraform Service on project: " + projname)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def disable_tf_on_project(url,username,password,projname):
    """
    Disable Terraform on Project

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    projname = Provide name of a Project to remove the Terraform service
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    proj_json = get_proj_by_name(url,username,password,projname)
    proj_id = proj_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}project-service/api/projects/{1}'.format(api_url_base,proj_id)
    data =  {
              "properties": {
              }
            }
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print("Successfully disabled Terraform Service on project: " + projname)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def remove_all_cz_from_project(url,username,password,projname):
    """
    Removes all CLoud Zones from project

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    proj_name = Provide name of a Project which to remove all Cloud Zones
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    proj_json = get_proj_by_name(url,username,password,projname)
    proj_id = proj_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}project-service/api/projects/{1}'.format(api_url_base,proj_id)
    data =  {
              "zoneAssignmentConfigurations": []
            }
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print("Removed ALL Cloud Zones from project: " + projname)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def delete_project(url,username,password,projname):
    """
    Delete Project

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    proj_name = Provide name of a Project to Delete
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    proj_json = get_proj_by_name(url,username,password,projname)
    proj_id = proj_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/projects/{1}'.format(api_url_base,proj_id)
    response = requests.delete(api_url, headers=headers, verify=False)
    if response.status_code == 204:
        print('Successfully Deleted Project: ' + projname)
        return 'Successfully Deleted Project: ' + projname
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

######Flavor Mappings######
def get_cloud_regionid_by_name(url,username,password,region_name):
    """
    Get Cloud Region Id for Further Configurations

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    region_name = Provide a name of Region to search for

    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/regions'.format(api_url_base,region_name)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            reg_name = json_data['content'][n]['externalRegionId']
            if reg_name == region_name:
                print("Found Cloud Zone: " + region_name)
                reg_id = json_data['content'][n]['id']
                return reg_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For Cloud Zone: " + region_name)
                return "No Match Found For Cloud Zone: " + region_name
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_cloud_flavor(url,username,password,flavor_name,mapping_name,cloud_instance_name,region_name):
    """
    Create Cloud Flavor
    Abstracts cloud images and assigns a size value to them (e.g. - small, medium, large)

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    flavor_name = Provide a name for the Flavor(e.g. - small, medium, etc.)

    size_name = Name

    cloud_size_name = Name of Cloud Size (e.g.- AWS: t2.small , Azure: Standard_B1ms, vSphere: 2:4 - CPU:MEM)

    region_name = Cloud Region (e.g. - Azure: eastus)

    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username,password)
    reg_id = get_cloud_regionid_by_name(url,username,password,region_name)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/flavor-profiles'.format(api_url_base)
    data =  {
                "name": flavor_name,
                "flavorMapping": {
                    mapping_name: {
                        "name": cloud_instance_name
                    }
                },
                "regionId": reg_id
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        print('Successfully Created Cloud Flavor')
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_flavor_by_name(url,username,password,flavor_name):
    """
    Get Flavor by name for further configurations

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    flavor_name = Name of the Flavor Mapping
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/flavor-profiles'.format(api_url_base,flavor_name)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            flav_name = json_data['content'][n]['name']
            if flav_name == flavor_name:
                print("Found Flavor Mapping: " + flavor_name)
                return json_data['content'][n]
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For Flavor Mapping: " + flavor_name)
                return "No Match Found For Flavor Mapping: " + flavor_name
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def update_cloud_flavor(url,username,password,flavor_name,mapping_name,cloud_instance_name):
    """
    Update Cloud Flavor

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    flavor_name = Name of the Flavor Mapping (i.e. aws)

    mapping_name = The name that displays in Cloud Assembly for the flavor (i.e.Small)

    cloud_instance_name = The name if the instance type from the public cloud (i.e. t2.small)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username,password)
    flav_json = get_flavor_by_name(url,username,password,flavor_name)
    flav_id = flav_json['id']
    current_flavors = flav_json['flavorMappings']['mapping']
    a = json.dumps(current_flavors)
    a = a[1:-1]
    new_flavor =  {mapping_name:{"name": cloud_instance_name}}
    b = json.dumps(new_flavor)
    b = b[1:-1]
    combined = a + "," + b
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/flavor-profiles/{1}'.format(api_url_base,flav_id)
    payload = "{" + '"' + "flavorMapping" + '"' + ":" " {"+ combined + "}}"
    data = json.loads(payload)
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print('Successfully Updated Cloud Flavor')
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_vsphere_flavor(url,username,password,flavor_name,mapping_name,cpu_count,mem_count,region_name):
    """
    Create vSphere Flavor
    vSphere Flavor is a size of an image, t-shirt sizing"

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    flavor_name = Name of the Flavor Mapping (i.e. vsphere)

    mapping_name = The name that displays in Cloud Assembly for the flavor (i.e.Small)

    cpu_count = number of CPUs assigned using this flavor (i.e. 2)

    mem_count = amount of memory assigned using this flavor in GB (i.e. 4)

    region_name = The datacenter id for the Cloud Account (i.e. Datacenter:datacenter-2)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username,password)
    reg_id = get_cloud_regionid_by_name(url,username,password,region_name)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/flavor-profiles'.format(api_url_base)
    data =  {
                "name": flavor_name,
                "flavorMapping": {
                    mapping_name: {
                        "cpuCount": cpu_count,
                        "memoryInMB": mem_count
                    }
                },
                "regionId": reg_id
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        json_data = json.loads(response.content.decode('utf-8'))
        print('Successfully Created vSphere Flavor')
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def update_vsphere_flavor(url,username,password,flavor_name,mapping_name,cpu_count,mem_count):
    """
    Update vSphere Flavor

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    flavor_name = Name of the Flavor Mapping (i.e. vsphere)

    mapping_name = The name that displays in Cloud Assembly for the flavor (i.e.Small)

    cpu_count = number of CPUs assigned using this flavor (i.e. 2)

    mem_count = amount of memory assigned using this flavor in GB (i.e. 4)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username,password)
    flav_json = get_flavor_by_name(url,username,password,flavor_name)
    flav_id = flav_json['id']
    current_flavors = flav_json['flavorMappings']['mapping']
    a = json.dumps(current_flavors)
    a = a[1:-1]
    new_flavor = {mapping_name:{"cpuCount": cpu_count,"memoryInMB": mem_count}}
    b = json.dumps(new_flavor)
    b = b[1:-1]
    combined = a + "," + b
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/flavor-profiles/{1}'.format(api_url_base,flav_id)
    payload = "{" + '"' + "flavorMapping" + '"' + ":" " {"+ combined + "}}"
    data = json.loads(payload)
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print('Successfully Updated vSphere Flavor')
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def delete_flavor_mapping(url,username,password,flavor_name):
    """
    Delete Flavor Mapping

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    flavor_name = Flavor name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    flav_json = get_flavor_by_name(url,username,password,flavor_name)
    flav_id = flav_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/flavor-profiles/{1}'.format(api_url_base,flav_id)
    response = requests.delete(api_url, headers=headers, verify=False)
    if response.status_code == 204:
        print('Successfully Deleted Flavor Mapping: ' + flavor_name)
        return 'Successfully Deleted Flavor Mapping: ' + flavor_name
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

######Image Mappings######
def create_image_mapping(url,username,password,profile_name,image_name,image_id,region_name):
    """
    Create Image Mapping.
    An image mapping ties a cloud image (AWS = AMI, vSphere = Template) to a Cloud Zone Region

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    profile_name = The name of the image profile (i.e.vsphere-images)

    image_name = The name of the image (i.e. Ubuntu)

    image_id = name of the image instance (i.e. ami-03659409b9c7d0c5f or vsphere-ubuntu-template)

    region_name = The datacenter id for the Cloud Account (i.e. Datacenter:datacenter-2 or eastus or us-west-1)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username,password)
    reg_id = get_cloud_regionid_by_name(url,username,password,region_name)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/image-profiles'.format(api_url_base)
    data =  {
              "name" : profile_name,
              "description": "Image Profile for " + profile_name,
              "imageMapping" : {
                image_name: {
                  "name": image_id
                }
              },
              "regionId": reg_id
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        json_data = json.loads(response.content.decode('utf-8'))
        print("Successfully Created Image Mapping: " + profile_name)
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_image_profile_by_name(url,username,password,profile_name):
    """
    Gets image mapping by name and reutns information via json

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    profile_name = The name of the image profile (i.e.vsphere-images)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/image-profiles'.format(api_url_base,profile_name)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            img_prof_name = json_data['content'][n]['name']
            if img_prof_name == profile_name:
                print("Found Image Mapping: " + profile_name)
                return json_data['content'][n]
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For Flavor Mapping: " + flavor_name)
                return "No Match Found For Flavor Mapping: " + flavor_name
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def update_image_mapping(url,username,password,profile_name,image_name,image_id):
    """
    Updates an existing Image Mapping.

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    profile_name = The name of the image profile (i.e.vsphere-images)

    image_name = The name of the image (i.e. Ubuntu)

    image_id = name of the image instance (i.e. ami-03659409b9c7d0c5f or vsphere-ubuntu-template)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username,password)
    img_json = get_image_profile_by_name(url,username,password,profile_name)
    img_id = img_json['id']
    current_image = img_json['imageMappings']['mapping']
    a = json.dumps(current_image)
    a = a[1:-1]
    new_image = {image_name: {"name": image_id}}
    b = json.dumps(new_image)
    b = b[1:-1]
    combined = a + "," + b
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/image-profiles/{1}'.format(api_url_base,img_id)
    payload = "{" + '"' + "imageMapping" + '"' + ":" " {"+ combined + "}}"
    data = json.loads(payload)
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print('Successfully Updated Image Mapping: ' + profile_name)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def delete_image_mapping(url,username,password,profile_name):
    """
    Delete Image Mapping

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    profile_name = Image Profile Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    img_json = get_image_profile_by_name(url,username,password,profile_name)
    img_id = img_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/image-profiles/{1}'.format(api_url_base,img_id)
    response = requests.delete(api_url, headers=headers, verify=False)
    if response.status_code == 204:
        print('Successfully Deleted Flavor Mapping: ' + profile_name)
        return 'Successfully Deleted Flavor Mapping: ' + profile_name
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

######Network Profiles######
def create_network_profile(url,username,password,region_name,net_profile_name):
    """
    Create Network Profile.

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    net_profile_name = The name of the network profile (i.e.vsphere-networks)

    region_name = The datacenter id for the Cloud Account (i.e. Datacenter:datacenter-2 or eastus or us-west-1)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    reg_id = get_cloud_regionid_by_name(url,username,password,region_name)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/network-profiles'.format(api_url_base)
    data = {
              "isolationType": "NONE",
              "tags": [],
              "customProperties": {
                "datacenterId": region_name
              },
              "name": net_profile_name,
              "regionId": reg_id
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        json_data = json.loads(response.content.decode('utf-8'))
        print('Successfully Created Network Profile: ' + net_profile_name)
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_netprofile_by_name(url,username,password,net_profile_name):
    """
    Get existing Network Profile by name and return information via json.

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    net_profile_name = The name of the network profile (i.e.vsphere-networks)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/network-profiles'.format(api_url_base,net_profile_name)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            prof_name = json_data['content'][n]['name']
            if prof_name == net_profile_name:
                print("Found Network Profile: " + net_profile_name)
                prof_id = json_data['content'][n]
                return prof_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For Network Profile: " + net_profile_name)
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_fabric_network_by_name(url,username,password,fabric_net_name):
    """
    Get discovered network by name and return information via json.

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    fabric_net_name = The name of the network that was discovered by vRA discover service (i.e.web-network)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/fabric-networks'.format(api_url_base,fabric_net_name)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            net_name = json_data['content'][n]['name']
            if net_name == fabric_net_name:
                print("Found Frabric Network: " + fabric_net_name)
                fabnet_id = json_data['content'][n]
                return fabnet_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For Frabric Network: " + fabric_net_name)
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def add_network_to_profile(url,username,password,region_name,net_profile_name,fabric_net_name):
    """
    Adds a discovered network to an existing Network Profile

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    net_profile_name = The name of the network profile (i.e.vsphere-networks)

    region_name = The datacenter id for the Cloud Account (i.e. Datacenter:datacenter-2 or eastus or us-west-1)

    fabric_net_name = The name of the network that was discovered by vRA discover service (i.e.web-network)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    reg_id = get_cloud_regionid_by_name(url,username,password,region_name)
    prof_json = get_netprofile_by_name(url,username,password,net_profile_name)
    fab_net_json = get_fabric_network_by_name(url,username,password,fabric_net_name)
    fab_net_id = fab_net_json['id']
    fab_id = []
    fab_id.append(fab_net_id)
    try:
        current_assigned_networks = prof_json['_links']['fabric-networks']['hrefs']
        for net in current_assigned_networks:
            net = net[26:]
            fab_id.append(net)
    except:
        print("Currently no networks assigned")
    prof_id = prof_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/network-profiles/{1}'.format(api_url_base,prof_id)
    data = {
              "fabricNetworkIds": fab_id
            }
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        print('Successfully Added Network to Network Profile: ' + net_profile_name)
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_cloud_acct_type(url,username,password,caid):
    """
    Returns the type of Cloud Account based on id. (used to determine NSX resources)

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    caid = Cloud Account ID
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/cloud-accounts/{1}'.format(api_url_base,caid)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        ca_type = extract_values(json_data,'cloudAccountType')
        return ca_type
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_nsxt_fabric_network_by_name(url,username,password,fabric_net_name):
    """
    Get discovered NSX-T network by name and return information via json.

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    fabric_net_name = The name of the network that was discovered by vRA discover service (i.e.web-network)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/fabric-networks'.format(api_url_base,fabric_net_name)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            net_name = json_data['content'][n]['name']
            if net_name == fabric_net_name:
                print("Found Frabric Network: " + fabric_net_name)
                ca_type = get_cloud_acct_type(url,username,password,json_data['content'][n]['cloudAccountIds'][0])
                if ca_type[0] == "nsxt":
                    print("Fabric Network is type NSXT")
                    fabnet_id = json_data['content'][n]
                    return fabnet_id
                    break
                elif n < end_n:
                    print("Frabric Network is not type NSXT")
                    n = n + 1
                elif n >= end_n:
                    print("No Match Found For NSXT Frabric Network: " + fabric_net_name)
                    break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For NSXT Frabric Network: " + fabric_net_name)
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def add_nsxt_network_to_profile(url,username,password,region_name,net_profile_name,fabric_net_name):
    """
    Adds a discovered NSX-T network to an existing Network Profile

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    net_profile_name = The name of the network profile (i.e.vsphere-networks)

    region_name = The datacenter id for the Cloud Account (i.e. Datacenter:datacenter-2 or eastus or us-west-1)

    fabric_net_name = The name of the network that was discovered by vRA discover service (i.e.web-network)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    reg_id = get_cloud_regionid_by_name(url,username,password,region_name)
    prof_json = get_netprofile_by_name(url,username,password,net_profile_name)
    fab_net_json = get_nsxt_fabric_network_by_name(url,username,password,fabric_net_name)
    fab_net_id = fab_net_json['id']
    fab_id = []
    fab_id.append(fab_net_id)
    try:
        current_assigned_networks = prof_json['_links']['fabric-networks']['hrefs']
        for net in current_assigned_networks:
            net = net[26:]
            fab_id.append(net)
    except:
        print("Currently no networks assigned")
    prof_id = prof_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/network-profiles/{1}'.format(api_url_base,prof_id)
    data = {
              "fabricNetworkIds": fab_id
            }
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        print('Successfully Added NSXT Network to Network Profile: ' + net_profile_name)
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def tag_fabric_network(url,username,password,fabric_net_name,tag_key,tag_value):
    """
    Tags a discovered network in vRA.

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    fabric_net_name = The name of the network that was discovered by vRA discover service (i.e.web-network)

    tag_key = The key for the tag (i.e env:tag_value)

    tag_value = Th value for the tag (i.e. tag_key:vsphere)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    fab_net_json = get_fabric_network_by_name(url,username,password,fabric_net_name)
    fab_net_id = fab_net_json['id']
    try:
        current_tags = fab_net_json['tags']
        new_tag = {"key": tag_key,"value": tag_value}
        current_tags.append(new_tag)
        tags = current_tags
    except:
        print("Currently no tags assigned")
        tags = []
        new_tag = {"key": tag_key,"value": tag_value}
        tags.append(new_tag)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/fabric-networks/{1}'.format(api_url_base,fab_net_id)
    data = {
              "tags": tags
            }
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        print('Successfully Tagged Fabric Network: ' + fabric_net_name)
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def config_ondemand_sec_groups_vsphere_network_profile(url,username,password,net_profile_name,edge_router_name,t0_router_name):
    """
    Configues vSphere network profile for on-demand security groups

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    net_profile_name = The name of the network profile (i.e.vsphere-networks)

    edge_router_name = Name of the edge router in NSX-T

    t0_router_name = Name of the T0 router in NSX-T
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    net_prof_json = get_netprofile_by_name(url,username,password,net_profile_name)
    net_prof_id = net_prof_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/network-profiles/{1}'.format(api_url_base,net_prof_id)
    current_dc_id = net_prof_json['customProperties']['datacenterId']
    edge_router_link = get_nsxt_router_link_by_name(url,username,password,edge_router_name)
    t0_router_link = get_nsxt_router_link_by_name(url,username,password,t0_router_name)
    data = {
            "isolationType": "SECURITY_GROUP",
            "customProperties": {
                "datacenterId": current_dc_id,
                "edgeClusterRouterStateLink": edge_router_link,
                "tier0LogicalRouterStateLink": t0_router_link
            }
           }
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        print('Successfully Configured On-Demand Security Group: ' + net_profile_name)
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_sec_group_by_name(url,username,password,secgroup_name):
    """
    Get discovered security group by name and return information via json.

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    secgroup_name = The name of the existing security group (i.e.web-security)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/security-groups'.format(api_url_base,secgroup_name)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            sg_name = json_data['content'][n]['name']
            if sg_name == secgroup_name:
                print("Found Security Group: " + secgroup_name)
                sg_id = json_data['content'][n]['id']
                return sg_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For Security Group: " + secgroup_name)
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def add_sec_group_vsphere_net_profile(url,username,password,net_profile_name,secgroup_name):
    """
    Adds discovered security group to a network profile.

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    net_profile_name = The name of the network profile (i.e.vsphere-networks)

    secgroup_name = The name of the existing security group (i.e.web-security)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    net_prof_json = get_netprofile_by_name(url,username,password,net_profile_name)
    net_prof_id = net_prof_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/network-profiles/{1}'.format(api_url_base,net_prof_id)
    try:
        current_secgroups = net_prof_json['_links']['security-groups']['hrefs']
        sec_groups = []
        for x in current_secgroups:
            x = x[26:]
            sec_groups.append(x)
        new_sec_group = get_sec_group_by_name(url,username,password,secgroup_name)
        sec_groups.append(new_sec_group)
    except:
        print("Currently no Security Groups assigned")
        sec_groups = []
        new_sec_group = get_sec_group_by_name(url,username,password,secgroup_name)
        sec_groups.append(new_sec_group)
    data = {
              "securityGroupIds": sec_groups
            }
    response = requests.patch(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        print('Successfully Added Security Group: ' + secgroup_name)
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def delete_netprofile(url,username,password,net_profile_name):
    """
    Delete Network Profile

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    net_profile_name = Network Profile Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    net_json = get_netprofile_by_name(url,username,password,net_profile_name)
    net_id = net_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/network-profiles/{1}'.format(api_url_base,net_id)
    response = requests.delete(api_url, headers=headers, verify=False)
    if response.status_code == 204:
        print('Successfully Deleted Network Profile: ' + net_profile_name)
        return 'Successfully Deleted Network profile: ' + net_profile_name
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

######Storage Profiles######
def get_vsphere_datastore_by_name(url,username,password,datastore_name):
    """
    Get vsphere datastore by name and return information via json.

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    datastore_name = The name of the datastore (i.e.sc2c01vsan01)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/fabric-vsphere-datastores'.format(api_url_base,datastore_name)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            ds_name = json_data['content'][n]['name']
            if ds_name == datastore_name:
                print("Found vSphere Datastore: " + datastore_name)
                ds_id = json_data['content'][n]
                return ds_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For vSphere Datastore: " + datastore_name)
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_storage_policy_id_by_name(url,username,password,policy_name):
    """
    Get storage policy id by name and return information via json.

    Arguments:


    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    policy_name = The name of the storage policy (i.e. "vSAN Default Storage Policy")
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/fabric-vsphere-storage-policies'.format(api_url_base,policy_name)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            sp_name = json_data['content'][n]['name']
            if sp_name == policy_name:
                print("Found vSphere Storage Polcy: " + policy_name)
                sp_id = json_data['content'][n]['id']
                return sp_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For vSphere Storage Policy: " + policy_name)
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_storage_profile_by_name(url,username,password,storage_profile_name):
    """
    Get Storage Profile by Name and return json information

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    storage_profile_name = Storage Profile Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/storage-profiles'.format(api_url_base,policy_name)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            sp_name = json_data['content'][n]['name']
            if sp_name == storage_profile_name:
                print("Found Storage Profile: " + storage_profile_name)
                sp_id = json_data['content'][n]
                return sp_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For Storage Profile: " + storage_profile_name)
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_vsphere_storage_profile(url,username,password,name,region_name,datastore_name,encrypted="false",sharelevel="normal",diskmode="independent-persistent",tag_key=None,iops_limit=None,tag_value=None,shares="1000",provision_type="thin",default="false",disktype="standard",policy_name=None):
    """
    Creates a vSphere Storage Profile

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    name = Name of the Storage Profile

    region_name = Name of the region this profile is attached (i.e Datacenter:datacenter-2)

    datastor_name = Name of the datastore to assign to profile

    encrypted = is datastore encrypted (true or false(default))

    sharelevel = Sets the share level (unspecified / low / normal(default) / high / custom)

    diskmode = Sets the disk mode for the profile (dependent / independent-persistent(default) / independent-nonpersistent)

    tag_key = Key for the tag (i.e. env:tag_value)

    tag_value = Value for the tag (i.e. tag_key:vsphere)

    iops_limit = Sets the IOPs limit for the Storage profile (if not set value is set to unlimited)

    shares = Sets the shares value for the storage profile (default is 1000)

    provision_type = Sets the provisioning type for the storage profile (unspecified / thin / thick / eagerZeroedThick)

    default = Is this the default profile for the region (true / false (default))

    disk_type = Type of disk for this profile (standard (default) / fcd)

    policy_name = The name of the storage policy from vCenter to use for this profile (if argument not added then datastore default policy is applied)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    reg_id = get_cloud_regionid_by_name(url,username,password,region_name)
    if tag_key != None:
        if tag_value != None:
            tag_prep = {"key": tag_key,"value": tag_value}
            tag = []
            tag.append(tag_prep)
    else:
        tag = []
    ds_json = get_vsphere_datastore_by_name(url,username,password,datastore_name)
    ds_id = ds_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/storage-profiles-vsphere'.format(api_url_base)
    payload = {
              "supportsEncryption": encrypted,
              "sharesLevel": sharelevel,
              "description": "vSphere Storage",
              "diskMode": diskmode,
              "tags": tag,
              "shares": shares,
              "provisioningType": provision_type,
              "regionId": reg_id,
              "name": name,
              "defaultItem": default,
              "diskType": disktype,
              "datastoreId": ds_id
            }
    if policy_name != None:
        policy_id = get_storage_policy_id_by_name(url,username,password,policy_name)
        a = json.dumps(payload)
        a = a[1:-1]
        policy = {"storagePolicyId": policy_id}
        b = json.dumps(policy)
        b = b[1:-1]
        combined = a + "," + b
        payload = "{" + combined + "}"
        payload = json.loads(payload)
    if iops_limit != None:
        c = json.dumps(payload)
        c = c[1:-1]
        iops = {"limitIops": iops_limit}
        d = json.dumps(iops)
        d = d[1:-1]
        combined = c + "," + d
        payload = "{" + combined + "}"
        payload = json.loads(payload)
    data = payload
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        print('Successfully Created vSphere Storage Profile')
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_aws_storage_profile(url,username,password,name,region_name,encrypted="false",devicetype="ebs",volumetype="standard",tag_key=None,iops_limit=None,tag_value=None,default="false"):
    """
    Creates a AWS Storage Profile

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    name = Name of the Storage Profile

    region_name = Name of the region this profile is attached (i.e us-west-1)

    encrypted = Is datastore encrypted (true or false(default))

    devicetype = The type of storage device to use (ebs / instance-store)

    volumetype = The type of volume (gp2 / io1 / sc1 / st1 / standard)

    tag_key = The key for the tag (i.e env:tag_value)

    tag_value = Th value for the tag (i.e. tag_key:aws)

    iops_limit = Sets the IOPs limit for the Storage profile (if not set value is set to unlimited)

    default = Is this the default profile for the region (true / false (default))
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    reg_id = get_cloud_regionid_by_name(url,username,password,region_name)
    if tag_key != None:
        if tag_value != None:
            tag_prep = {"key": tag_key,"value": tag_value}
            tag = []
            tag.append(tag_prep)
    else:
        tag = []
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/storage-profiles-aws'.format(api_url_base)
    payload = {
                  "deviceType": devicetype,
                  "volumeType": volumetype,
                  "supportsEncryption": encrypted,
                  "regionId": reg_id,
                  "name": name,
                  "description": "AWS Storage Profile",
                  "defaultItem": default,
                  "tags": tag
                }
    if iops_limit != None:
        c = json.dumps(payload)
        c = c[1:-1]
        iops = {"limitIops": iops_limit}
        d = json.dumps(iops)
        d = d[1:-1]
        combined = c + "," + d
        payload = "{" + combined + "}"
        payload = json.loads(payload)
    data = payload
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        print('Successfully Created AWS Storage Profile')
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_azure_storage_profile(url,username,password,name,region_name,encrypted="false",disktype="Standard_LRS",diskcaching="None",oscaching="None",tag_key=None,tag_value=None,default="false"):
    """
    Creates a Azure Storage Profile

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    name = Name of the Storage Profile

    region_name = Name of the region this profile is attached (i.e us-west-1)

    encrypted = Is datastore encrypted (true or false(default))

    disktype = The type of storage device to use (Standard_LRS / Premium_LRS)

    diskcaching = Cache the data disk? (None / ReadOnly / ReadWrite)

    oscaching = Cache the OS disk? (None / ReadOnly / ReadWrite)

    tag_key = The key for the tag (i.e env:tag_value)

    tag_value = Th value for the tag (i.e. tag_key:azure)

    default = Is this the default profile for the region (true / false (default))
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    reg_id = get_cloud_regionid_by_name(url,username,password,region_name)
    if tag_key != None:
        if tag_value != None:
            tag_prep = {"key": tag_key,"value": tag_value}
            tag = []
            tag.append(tag_prep)
    else:
        tag = []
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/storage-profiles-azure'.format(api_url_base)
    data = {
             "supportsEncryption": encrypted,
             "regionId": reg_id,
             "name": name,
             "description": "Azure Storage Profile",
             "defaultItem": default,
             "diskType": disktype,
             "dataDiskCaching": diskcaching,
             "osDiskCaching": oscaching,
             "tags": tag
           }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        print('Successfully Created Azure Storage Profile')
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

######Integrations######
def create_actions_content_source(url,username,password,name,int_name,proj_name,repo,branch,path):
    """
    Creates an action content source on a github integration

    Arguments:


    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    name = Name of the content source (i.e. ABC Actions)

    int_name = Name of the integration (i.e. ABC GitHub Integration)

    proj_name = Name of vRA Project to associate content source

    repo = Name of the github repository

    branch = Name of branch in repo (i.e. master)

    path = path to folder of actions (i.e actions)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    proj_json = get_proj_by_name(url,username,password,proj_name)
    proj_id = proj_json['id']
    int_id = get_integration_by_name(url,username,password,int_name)
    api_url = '{0}content/api/sources'.format(api_url_base)
    data =  {
              "name": name,
              "typeId": "com.github",
              "syncEnabled" : "true",
              "projectId" : proj_id,
              "config": {
                "integrationId" : int_id,
                "repository" : "mcclanc/vra8-content",
                "path" : path,
                "branch" : "master",
                "contentType" : "abx_scripts"
              }
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        print('Successfully Created Actions Content Source')
        return 'Successfully Created Actions Content Source'
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_blueprint_content_source(url,username,password,name,int_name,proj_name,repo,branch,path):
    """
    Creates a cloud template content source on a github integration

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    name = Name of the content source (i.e. ABC Actions)

    int_name = Name of the integration (i.e. ABC GitHub Integration)

    proj_name = Name of vRA Project to associate content source

    repo = Name of the github repository

    branch = Name of branch in repo (i.e. master)

    path = Folder name storing cloud templates in repo (i.e templates)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    proj_json = get_proj_by_name(url,username,password,proj_name)
    proj_id = proj_json['id']
    int_id = get_integration_by_name(url,username,password,int_name)
    api_url = '{0}content/api/sources'.format(api_url_base)
    data =  {
              "name": name,
              "typeId": "com.github",
              "syncEnabled" : "true",
              "projectId" : proj_id,
              "config": {
                "integrationId" : int_id,
                "repository" : "mcclanc/vra8-content",
                "path" : path,
                "branch" : "master",
                "contentType" : "blueprint"
              }
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        print('Successfully Created Blueprint Content Source')
        return 'Successfully Created Blueprint Content Source'
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def delete_storage_profile(url,username,password,storage_profile_name):
    """
    Delete Storage Profile

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    storage_profile_name = Storage Profile Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    sp_json = get_storage_profile_by_name(url,username,password,storage_profile_name)
    sp_id = sp_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}iaas/api/storage-profiles/{1}'.format(api_url_base,sp_id)
    response = requests.delete(api_url, headers=headers, verify=False)
    if response.status_code == 204:
        print('Successfully Deleted Storage Profile: ' + storage_profile_name)
        return 'Successfully Deleted Storage Profile: ' + storage_profile_name
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

######Blueprint Version and Release######
def get_template_by_name(url,username,password,template_name):
    """
    Finds the cloud template by name and returns information via json

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    template_name = Name of the cloud template to find
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}blueprint/api/blueprints'.format(api_url_base)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            templt_name = json_data['content'][n]['name']
            if templt_name == template_name:
                print("Found Cloud Template: " + template_name)
                template_id = json_data['content'][n]
                return template_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For Cloud Template: " + template_name)
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_template_version(url,username,password,template_name,version,release="false",change_log=None):
    """
    Creates a version of the cloud template

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    template_name = Name of the cloud template to find

    version = version for the template (i.e. 1.1)

    release = Release the version to the Service Broker catalog (true / false (default))

    change_log = Description of changes to template (if not included the change log is left blank)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    template_json = get_template_by_name(url,username,password,template_name)
    template_id = template_json['id']
    api_url = '{0}blueprint/api/blueprints/{1}/versions'.format(api_url_base,template_id)
    if change_log == None:
        change_log = ""
    data =  {
              "changeLog": change_log,
              "description": "Created version " + version + " of Template",
              "release": release,
              "version": version
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        print('Successfully Created Version of Cloud Template')
        return 'Successfully Created Version of Cloud Template'
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def release_template_version(url,username,password,template_name,version):
    """
    Releases a version of the cloud template to the Service Broker catalog

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    template_name = Name of the cloud template to find

    version = version for the template (i.e. 1.1)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    template_json = get_template_by_name(url,username,password,template_name)
    template_id = template_json['id']
    api_url = '{0}blueprint/api/blueprints/{1}/versions/{2}/actions/release'.format(api_url_base,template_id,version)
    response = requests.post(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        print('Successfully Released Version of Cloud Template to Catalog')
        return 'Successfully Released Version of Cloud Template to Catalog'
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def delete_template(url,username,password,template_name):
    """
    Delete Cloud Template

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    template_name = Cloud Template Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    temp_json = get_template_by_name(url,username,password,template_name)
    temp_id = temp_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}blueprint/api/blueprints/{1}'.format(api_url_base,temp_id)
    response = requests.delete(api_url, headers=headers, verify=False)
    if response.status_code == 204:
        print('Successfully Deleted Cloud Template: ' + template_name)
        return 'Successfully Deleted Cloud Template: ' + template_name
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

##########Service Broker##########
def create_sb_content_source(url,username,password,name,proj_name,content_type):
    """
    Creates Content Source in Service Broker

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    name = Content Source name

    proj_name = vRA Project name

    content_type = PIPELINE / TEMPLATE / ABX / VRO
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    proj_json = get_proj_by_name(url,username,password,proj_name)
    proj_id = proj_json['id']
    if content_type == "PIPELINE":
        content_type = "com.vmw.codestream"
    if content_type == "TEMPLATE":
        content_type = "com.vmw.blueprint"
    if content_type == "ABX":
        content_type = "com.vmw.abx.actions"
    if content_type == "VRO":
        content_type = "com.vmw.vro.workflow"
    api_url = '{0}catalog/api/admin/sources'.format(api_url_base)
    data =  {
              "config": {
                "sourceProjectId": proj_id
              },
              "typeId": content_type,
              "name": name
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        print('Successfully Created Service Broker Content Source: ' + name)
        return 'Successfully Created Actions Content Source: ' + name
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_sb_content_source_by_name(url,username,password,content_source_name):
    """
    Finds the Service Broker content source by name and returns information via json

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    content_source_name = The name used to create the content source in Service Broker
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}catalog/api/admin/sources'.format(api_url_base)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['numberOfElements']
        end_n = end_n - 1
        while True:
            source_name = json_data['content'][n]['name']
            if source_name == content_source_name:
                print("Found Content Source: " + content_source_name)
                source_id = json_data['content'][n]
                return source_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No Match Found For Frabric Network: " + content_source_name)
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_sb_content_source(url,username,password,proj_name,content_source_name):
    """
    Adds Entitlement to the Project for a Service Broker content source

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    proj_name = vRA Project name

    content_source_name = The name used to create the content source in Service Broker
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    proj_json = get_proj_by_name(url,username,password,proj_name)
    proj_id = proj_json['id']
    cs_json = get_sb_content_source_by_name(url,username,password,content_source_name)
    cs_id = cs_json['id']
    api_url = '{0}catalog/api/admin/entitlements'.format(api_url_base)
    data =  {
              "projectId": proj_id,
              "definition": {
                "id": cs_id,
                "sourceName": content_source_name,
                "type": "CatalogSourceIdentifier"
              }
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 201:
        print('Successfully Entitled Content Source: ' + content_source_name)
        return 'Successfully Entitled Content Source: ' + content_source_name
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def delete_sb_content_source(url,username,password,content_source_name):
    """
    Delete Service Broker Content Source

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    content_source_name = Content Source Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    cs_json = get_sb_content_source_by_name(url,username,password,content_source_name)
    cs_id = cs_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}catalog/api/admin/sources/{1}'.format(api_url_base,cs_id)
    response = requests.delete(api_url, headers=headers, verify=False)
    if response.status_code == 204:
        print('Successfully Deleted Service Broker Content Source: ' + content_source_name)
        return 'Successfully Deleted Service Broker Content Source: ' + content_source_name
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_polid_by_name(url,username,password,polname):
    """
    Retrieve Policy ID by name For Further Configurations

    Arguments:

    url = vRA FQDN

    username = vRA Admin User

    password = vRA Admin Password

    polname = Policy Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}policy/api/policies'.format(api_url_base)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['totalElements']
        end_n = end_n - 1
        while True:
            pol_name = json_data['content'][n]['name']
            if pol_name == polname:
                print("Found Policy " + polname)
                pl_id = json_data['content'][n]['id']
                return pl_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No match found for policy: " + polname)
                return "No match found for policy: " + polname
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def delete_policy(url,username,password,polname):
    """
    Delete Policy

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    polname = Policy Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username,password,czname)
    pz_id = get_polid_by_name(url,username,password,polname)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}policy/api/policies/{1}'.format(api_url_base,pz_id)
    response = requests.delete(api_url, headers=headers, verify=False)
    if response.status_code == 204:
        print("Successfully Deleted Policy: " + polname)
        return "Successfully Deleted Policy: " + polname
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_catalog_item_by_name(url,username,password,item_name):
    """
    Retrieve a catalog item by name and return information via json

    Arguments:

    url = vRA FQDN

    username = vRA Admin User

    password = vRA Admin Password

    item_name = Catalog Item Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}catalog/api/items'.format(api_url_base)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['numberOfElements']
        end_n = end_n - 1
        while True:
            cat_name = json_data['content'][n]['name']
            if cat_name == item_name:
                print("Found Catalog Item " + item_name)
                cat_id = json_data['content'][n]
                return cat_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No match found for Catalog Item : " + item_name)
                return "No match found for Catalog Item : " + item_name
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def request_catalog_item(url,username,password,proj_name,item_name,deployment_name,input_json,reason=None,version=None):
    """
    Request a catalog item for deployment

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    proj_name = vRA Project name

    item_name = Name of the Catalog item to request

    deployment_name = The name you want to provide for the deployment

    input_json = Inpus for the catalog request in json format (i.e. {"machine_name": "machine1","image": "ubuntu"})

    reason = Reason for the deployment (This is not required)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    proj_json = get_proj_by_name(url,username,password,proj_name)
    proj_id = proj_json['id']
    item_json = get_catalog_item_by_name(url,username,password,item_name)
    item_id = item_json['id']
    if version == None:
        version = ""
    if reason == None:
        reason = ""
    api_url = '{0}catalog/api/items/{1}/request'.format(api_url_base,item_id)
    data =  {
              "bulkRequestCount": 1,
              "deploymentName": deployment_name,
              "inputs": input_json,
              "projectId": proj_id,
              "reason": reason,
              "version": version
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print('Successfully Deployed Catalog Item: ' + item_name + ' with deployment name ' + deployment_name)
        return 'Successfully Deployed Catalog Item: ' + item_name + ' with deployment name ' + deployment_name
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_deployment_by_name(url,username,password,dep_name):
    """
    Retrieve an existing deployment by name and return information via json

    Arguments:

    url = vRA FQDN

    username = vRA Admin User

    password = vRA Admin Password

    dep_name = Name of the Deployment
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}deployment/api/deployments'.format(api_url_base)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        n = 0
        end_n = json_data['numberOfElements']
        end_n = end_n - 1
        while True:
            dp_name = json_data['content'][n]['name']
            if dp_name == dep_name:
                print("Found Catalog Item " + dep_name)
                dp_id = json_data['content'][n]
                return dp_id
                break
            elif n < end_n:
                n = n + 1
            elif n >= end_n:
                print("No match found for Deployment : " + dep_name)
                return "No match found for zdeployment : " + dep_name
                break
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def delete_deployment(url,username,password,dep_name):
    """
    Deletes an existing deployment

    Arguments:

    url = vRA FQDN

    username = vRA Admin User

    password = vRA Admin Password

    dep_name = Name of the Deployment
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    dep_json = get_deployment_by_name(url,username,password,dep_name)
    dep_id = dep_json['id']
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}deployment/api/deployments/{1}'.format(api_url_base,dep_id)
    response = requests.delete(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        print('Successfully Deleted Deployment: ' + dep_name)
        return 'Successfully Deleted Deployment: ' + dep_name
    else:
        print(response.status_code)
        return response.status_code

def create_lease_policy(url,username,password,polname,projname,enftype,operator,item_name,leasegrace=15,leaseterm=30,leasemax=90):
    """
    Create Service Broker Lease Policy

    Arguments:

    url = vRA FQDN

    username = vRA Admin

    password = vRA Admin Password

    pol_name = Policy Name

    pol_type = Policy Type

    projname = Project Name to tie to Policy

    enftype = Default "HARD, can be "SOFT"

    operator: "eq" or "not eq" (equals or not equals)

    item_name: Catalog Item Name to apply criteria too

    leasegrace: Lease Grace Period (default = 15 days)

    leaseterm: Lease Term Period (default = 30 days)

    leasemax: Max Lease Period (default = 90 days)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url, username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    proj_json = get_proj_by_name(url,username,password,projname)
    proj_id = proj_json['id']
    catitem_json = get_catalog_item_by_name(url,username,password,item_name)
    catitem_id = catitem_json['id']
    api_url = '{0}policy/api/policies/'.format(api_url_base)
    data = {
            "name": polname,
            "projectId": proj_id,
            "definition":{
                "leaseGrace": leasegrace,
                "leaseTermMax": leaseterm,
                "leaseTotalTermMax": leasemax
            },
            "enforcementType": enftype,
            "typeId":"com.vmware.policy.deployment.lease",
            "criteria":{
                "matchExpression":{
                    "key":"catalogItemId",
                    "operator": operator,
                    "value": catitem_id
                }
            }
        }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        print("Successfully Created Lease Policy")
        return None
    else:
        print(response.status_code)
        return response.status_code

def create_approval_policy(url,username,password,polname,projname,enftype,operator,item_name,level=1,expiry=5):
    """
    Create Service Broker Approval Policy

    Arguments:

    url = vRA FQDN

    username = vRA Admin

    password = vRA Admin Password

    pol_name = Policy Name

    pol_type = Policy Type

    projname = Project Name to tie to Policy

    enftype = Default "HARD, can be "SOFT"

    key = evaluator, (e.g. - eq, notEq, hasAny) refer to vRA Documentation for more options

    value = The object or value that you want to filter the criteria by (e.g. - Cloud Template Name, user, Cloud Account etc.)see vRA Documentation
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url, username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    proj_json = get_proj_by_name(url,username,password,projname)
    proj_id = proj_json['id']
    catitem_json = get_catalog_item_by_name(url,username,password,item_name)
    catitem_id = catitem_json['id']
    api_url = '{0}policy/api/policies/'.format(api_url_base)
    data = {
              "name": polname,
              "projectId": proj_id,
              "definition": {
                "level": level,
                "approvalMode": "ANY_OF",
                "autoApprovalDecision": "APPROVE",
                "approvers": [
                  "USER:configuser"
                ],
                "autoApprovalExpiry": expiry,
                "actions": [
                  "Deployment.Create"
                ]
              },
              "enforcementType": enftype,
              "typeId": "com.vmware.policy.approval",
              "criteria": {
                "matchExpression": {
                  "key": "catalogItemId",
                  "operator": operator,
                  "value": catitem_id
                }
              }
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        print("Successfully Created Approval Policy")
        return None
    else:
        print(response.status_code)
        print(response.text)
        return response.status_code

def create_action_policy(url,username,password,polname,projname,enftype,operator,action,item_name):
    """
    Create Service Broker Day 2 Action

    Arguments:

    url = vRA FQDN

    username = vRA Admin

    password = vRA Admin Password

    pol_name = Policy Name

    projname = Project Name to tie to Policy

    enftype = Default "HARD, can be "SOFT"

    operator = "eq" or "not eq" (equals or does not equal)

    action = Day 2 Action, e.g. "Deployment.Delete" see vRA Documentation for various Day 2 Actions

    item_name = catalog item that you want to apply policy to
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url, username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    proj_json = get_proj_by_name(url,username,password,projname)
    proj_id = proj_json['id']
    catitem_json = get_catalog_item_by_name(url,username,password,item_name)
    catitem_id = catitem_json['id']
    api_url = '{0}policy/api/policies'.format(api_url_base)
    data =  {
                "name": polname,
                "projectId": proj_id,
                "definition":{
                    "allowedActions":[
                        {
                            "authorities":[
                                "ROLE:administrator"
                            ],
                            "actions":[
                                action
                            ]
                        }
                    ]
                },
                "enforcementType": enftype,
                "typeId":"com.vmware.policy.deployment.action",
                "criteria":{
                    "matchExpression":{
                        "key":"catalogItemId",
                        "operator": operator,
                        "value": catitem_id
                    }
                }
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        print("Successfully Created Action Policy")
        return None
    else:
        print(response.status_code)
        print(response.text)
        return response.status_code

######Code Stream######
def create_cs_variable(url,username,password,name,proj_name,type,value,description=None):
    """
    Creates a Code Stream variable

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    name = Name of the Variable

    proj_name = Name of the project the variable is assocaited

    type = type of vairable to create (REGULAR / RESTRICTED / SECRET)

    value = Value of the variable
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}codestream/api/variables'.format(api_url_base)
    if description == None:
        description = ""
    data =  {
              "description": description,
              "name": name,
              "project": proj_name,
              "type": type,
              "value": value
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print('Successfully Created Code Stream Variable')
        return 'Successfully Created Code Stream Variable'
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_variable_by_name(url,username,password,variable_name):
    """
    Get Storage Profile by Name and return json information

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    storage_profile_name = Storage Profile Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}codestream/api/variables'.format(api_url_base)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        var_links = json_data['links']
        for x in var_links:
            var_name = json_data['documents'][x]['name']
            if var_name == variable_name:
                print("Found variable: " + variable_name)
                var_id = json_data['documents'][x]['id']
                return var_id
            else:
                print("Variable " + variable_name + " not found!")
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def delete_variable(url,username,password,variable_name):
    """
    Delete Code Stream Variable

    Arguments:
    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    variable_name = Variable Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    var_id = get_variable_by_name(url,username,password,variable_name)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}codestream/api/variables/{1}'.format(api_url_base,var_id)
    response = requests.delete(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        print('Successfully Deleted Code Stream Variable: ' + variable_name)
        return 'Successfully Deleted Code Stream Variable: ' + variable_name
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

##########Functions Using NON-PUBLIC API Calls##########
def get_nsxt_router_link_by_name(url,username,password,router_name):
    """
    Gets the document link to the NSX-T router by name and return the link

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    router_name = Name of the router in NSX-T (i.e. T0-router)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}provisioning/uerp/resources/routers'.format(api_url_base)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        router_links = json_data['documentLinks']
        for x in router_links:
            api_url = '{0}provisioning/uerp{1}'.format(api_url_base,x)
            response = requests.get(api_url, headers=headers, verify=False)
            if response.status_code == 200:
                json_data = json.loads(response.content.decode('utf-8'))
                rtr_name = json_data['name']
                if rtr_name == router_name:
                    print("Found NSXT Router by name: " + router_name)
                    return x
            else:
                print("Inner Rest call for get_nsxt_router_link_by_name failed with error: " + response.status_code)
                return ("Inner Rest call for get_nsxt_router_link_by_name failed with error: " + response.status_code)
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_github_saas_integration(url,username,password,name,private_key):
    """
    Creates Github integration in Cloud Assembly

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    name = Name of the Github integration (i.e. ABC Github)

    private_key = Private key created in Github for secure access
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}provisioning/uerp/provisioning/mgmt/endpoints?external='.format(api_url_base)
    data =  {
                "endpointProperties": {
                    "url": "www.github.com",
                    "privateKey": private_key
                },
                "customProperties": {
                    "isExternal": "true"
                },
                "endpointType": "com.github.saas",
                "name": name
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False, timeout=5)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        print('Successfully Created GitHub SaaS Integration')
        return json_data
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def get_integration_by_name(url,username,password,int_name):
    """
    Gits a Cloud Assembly Integration by name and returns information via json

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    int_name = Name of the Integration in Cloud Assembly (i.e. ABC Github)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}provisioning/uerp/resources/endpoints'.format(api_url_base)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        endpoint_links = json_data['documentLinks']
        for x in endpoint_links:
            api_url = '{0}provisioning/uerp{1}'.format(api_url_base,x)
            response = requests.get(api_url, headers=headers, verify=False)
            if response.status_code == 200:
                json_data = json.loads(response.content.decode('utf-8'))
                integration_name = json_data['name']
                if integration_name == int_name:
                    print("Found Integration by name: " + int_name)
                    int_id = x[21:]
                    return int_id
            else:
                print("Inner Rest call for get_nsxt_router_link_by_name failed with error: " + response.status_code)
                return ("Inner Rest call for get_nsxt_router_link_by_name failed with error: " + response.status_code)
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_ansible_oss_integration(url,username,password,name,private_key,private_id,hostname,inventory_path,use_sudo="true",ssh_port="22"):
    """
    Creates an Ansible Open Source integration in Cloud Assembly

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    name = Name of the Ansible OSS integration

    private_key = Password used for integration

    private_id = Username used for integration

    hostname = FQDN or IP of Ansible Server

    inventory_path = Path to inventory file on ansible server

    use_sudo = Use sudo when running commands (default is true)

    ssh_port = Port Ansible will use to run commands on machines (default is port 22)
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}provisioning/uerp/provisioning/mgmt/endpoints?external'.format(api_url_base)
    data =  {
              "endpointProperties": {
                "hostName": hostname,
                "dcId": "onprem",
                "inventoryFilePath": inventory_path,
                "privateKeyId": private_id,
                "privateKey": private_key,
                "useSudo": use_sudo,
                "location": "Private",
                "sshPort": ssh_port,
                "acceptSelfSignedCertificate": "true"
              },
              "customProperties": {
                "isExternal": "true"
              },
              "endpointType": "ansible",
              "associatedEndpointLinks": [],
              "name": name,
              "tagLinks": []
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print('Successfully Created Ansible OSS Integration')
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def create_ansibletower_integration(url,username,password,name,private_key,private_id,hostname,use_sudo="true",ssh_port="22"):
    """
    Creates an Ansible Open Source integration in Cloud Assembly

    Arguments:

    url = vRA FQDN

    username = vRA Admin user

    password = vRA Admin password

    name = Name of the Ansible OSS integration

    private_key = Password used for integration

    private_id = Username used for integration

    hostname = FQDN or IP of Ansible Server
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}provisioning/uerp/provisioning/mgmt/endpoints?external'.format(api_url_base)
    data =  {
              "endpointProperties": {
                "hostName": hostname,
                "dcId": "onprem",
                "privateKeyId": private_id,
                "privateKey": private_key,
                "location": "Private",
                "acceptSelfSignedCertificate": "true"
              },
              "customProperties": {
                "isExternal": "true"
              },
              "endpointType": "ansible.tower",
              "associatedEndpointLinks": [],
              "name": name,
              "tagLinks": []
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print('Successfully Created Ansible Tower Integration')
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

def delete_integration_by_name(url,username,password,int_name):
    """
    Delete Integration in vRA Cloud Assembly

    Arguments:

    url = vRA FQDN

    username = vRA admin user

    password = vRA Admin password

    int_name = Integration Name
    """
    api_url_base = set_bas_url(url)
    access_key = get_token(url,username, password)
    int_id = get_integration_by_name(url,username,password,int_name)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(access_key)}
    api_url = '{0}provisioning/uerp/resources/endpoints/{1}'.format(api_url_base,cs_id)
    response = requests.delete(api_url, headers=headers, verify=False)
    if response.status_code == 204:
        print('Successfully Deleted Integration in Cloud Assembly: ' + content_source_name)
        return 'Successfully Deleted Integration in Cloud Assembly: ' + content_source_name
    else:
        print(response.status_code)
        json_data = json.loads(response.content.decode('utf-8'))
        return json_data

#url = "vra8-dev-ga.cmbu.local"
#username = "configuser"
#password = "VMware1!"
