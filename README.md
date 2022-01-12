# Pre-requisites:
1. Python3 needs to be installed
Most linux and macos distributions will have python3 already.
For windows, please follow the download instructions from here: https://www.python.org/downloads/release/python-395/
2. The input file needs to be a flat file. A sample file is provided here, named ip_list.txt
3. Active WaaS account
4. Application under which the configuration change is required to be done.
5. As with any python scripts, its recommended that this script be executed in a python virtual environment. Unzip the contents of the file and activate the virtual env : `source bin/activate`
6. Install the python packages: `pip3 install -r requirements.txt`

# Usage details:

Command: waas_ip_upload.py [-h] [-u USERNAME] [-f FILENAME] [-a ACTION]
                         [-s SERVICE_APP_NAME]
Example: `python3 waas_ip_upload.py -u test@company.com -f ip_list.txt -a block -s test_svc_rulesetstaging`

Arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Email address to login to Barracuda WaaS
  -f FILENAME, --filename FILENAME
                        Input file containing the list of ip addresses
  -a ACTION, --action ACTION
                        Whether to allow or block the ip addresses. Defaults
                        to 'allow'. Allowed values are 'allow' or 'block'
  -s SERVICE_APP_NAME, --service_app_name SERVICE_APP_NAME
                        Service name into which configuration needs to be
                        updates
# Support
For any questions, connect with wafsupport_team@barracuda.com