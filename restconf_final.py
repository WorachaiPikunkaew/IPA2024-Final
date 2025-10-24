import json
import requests
requests.packages.urllib3.disable_warnings()

# IP address context
def set_ip(ip_address):
    global api_url
    api_url= "https://"+ip_address+"/restconf/data/ietf-interfaces:interfaces"


# Router IP Address is 10.0.15.181-184
# api_url = "https://10.0.15.61/restconf/data/ietf-interfaces:interfaces"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}
basicauth = ("admin", "cisco")


def create():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070177",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.1.77.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            }
        }
    }

    resp = requests.post(
            api_url, 
            data=json.dumps(yangConfig), 
            auth=basicauth, 
            headers=headers, 
            verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback66070177 is created successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot create: Interface loopback 66070177"


def delete():
    resp = requests.delete(
        api_url+"/interface=Loopback66070177", 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070177 is deleted successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback 66070177"


def enable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070177",
            "enabled": True
        }
    }

    resp = requests.patch(
        api_url+"/interface=Loopback66070177", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070177 is enabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback 66070177"


def disable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070177",
            "enabled": False
        }
    }

    resp = requests.patch(
        api_url+"/interface=Loopback66070177", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "interface loopback 66070177 is disabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot disable: Interface loopback 66070177"


def status():
    api_url_status = "https://10.0.15.61/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070177"

    resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json['ietf-interfaces:interface']['admin-status']
        oper_status = response_json['ietf-interfaces:interface']['oper-status']
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 66070177 is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 66070177 is disabled"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback 66070177"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot get status of Interface loopback 66070177"
