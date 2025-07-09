import requests

requests.packages.urllib3.disable_warnings()

device = {
    "host": "10.0.0.29",
    "port": "443",
    "user": "dylan",
    "password": "password1"
}

headers = {
    "Accept": "application/yang-data+json"
}

url = f'https://{device["host"]}:{device["port"]}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface=GigabitEthernet1'

response = requests.get(url=url, headers=headers, auth=(device['user'], device['password']), verify=False)
response.raise_for_status()
print(response.text)
