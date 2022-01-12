import requests
import json
import sys
import logging
import argparse
import getpass

logging.basicConfig(level = logging.DEBUG, filename = 'output.log')

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--username", help="Email address to login to Barracuda WaaS")
parser.add_argument("-f", "--filename", help="Input file containing the list of ip addresses")
parser.add_argument("-a", "--action", help="Whether to allow or block the ip addresses. Defaults to 'allow'. Allowed values are 'allow' or 'block'")
parser.add_argument("-s", "--service_app_name", help="Service name into which configuration needs to be updates")
password=getpass.getpass()

args = parser.parse_args()
def waas_login():
    base_url = "https://api.waas.barracudanetworks.com/v2/waasapi/"
    login_req_url = base_url + "api_login/"
    data = {"email": f'{args.username}', "password": f'{password}'}
    login_req = requests.post(login_req_url, data=data)

    login_response = login_req.json()
    token = login_response['key']
    headers = {"Content-Type": "application/json", "auth-api": f'{token}'}
    login_info = {"base_url": base_url, "headers": headers}
    return login_info

login_info = waas_login()

# Parsing the file contents
input = args.filename
with open(f'{input}', 'r') as f:
    input_file = f.readlines()

exceptions = []

action = args.action
if action == "allow":
    value = True
elif action == "block":
    value = False
else:
    value = True


for content in range(len(input_file)):
    exceptions.append({
      "allow": value,
      "ip": f"{input_file[content]}",
      "netmask": "255.255.255.255"
    })


#IP Upload request
app_url = login_info["base_url"] + "applications/"
get_app_info = requests.get(app_url, headers=login_info["headers"])
get_app_info_resp = get_app_info.json()
app_id_info = get_app_info_resp['results']
logging.info(args.service_app_name)
for count in range(len(app_id_info)):
    if app_id_info[count]['name'] == args.service_app_name:
        app_id = app_id_info[count]['id']
        logging.info(app_id)
        upload_url = login_info["base_url"] +"applications/"+ f'{app_id}' +"/ip_reputation/"
        logging.info(upload_url)
        current_ip_list_req = requests.get(upload_url, headers=login_info["headers"])
        current_ip_list_resp = current_ip_list_req.json()
        current_exceptions = []
        current_exceptions = current_ip_list_resp["exceptions"]
        logging.info("\n...Existing ip list...\n")
        logging.info(current_exceptions)
        logging.info("\n...List added in this task...\n")
        logging.info(exceptions)
        for ip_entry_num in range(len(exceptions)):
            current_exceptions.append(exceptions[ip_entry_num])
        logging.info("\n...Updated IP list... \n")
        logging.info(current_exceptions)

        data = {
            "block_satellite_providers": current_ip_list_resp["block_satellite_providers"],
            "managed_service": 1,
            "block_barracuda_reputation_blacklist": current_ip_list_resp["block_barracuda_reputation_blacklist"],
            "blocked_countries": current_ip_list_resp["blocked_countries"],
            "block_anonymous_proxies": current_ip_list_resp["block_anonymous_proxies"],
            "block_tor_nodes": current_ip_list_resp["block_tor_nodes"],
            "exceptions": current_exceptions,
            "enabled": current_ip_list_resp["enabled"]
            }
        #print(data)
        upload_req = requests.patch(upload_url, headers=login_info["headers"], data=json.dumps(data))
        logging.info(upload_req.text)
    else:
        pass



    