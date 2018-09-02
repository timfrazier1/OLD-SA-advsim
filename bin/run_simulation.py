import os
import sys
import json
#just set up reference to our apps on-disk location explicitly
#so we can import local libs as needed
from splunk.clilib.bundle_paths import make_splunkhome_path

fire_search = "|makeresults | eval os=\"windows\", test_id=\"{test_id}\", dest=\"{dest_addr}\""
# example search
# |makeresults | eval os="windows", test_id="T1155", dest="192.169.1.1" 
# | sendalert sendtophantom param.phantom_server="automation (https://34.204.5.46)" param.severity="medium" param.sensitivity="amber"
# param.phantom_server= should be retireved programattically from 
# /servicesNS/nobody/phantom/configs/conf-phantom/phantom?output_mode=json
# phantom_server = json.load(sys.stdin)["entry"][0]["content"]["value"]
# phantom_server = json.loads(phantom_server).keys()[0]

if sys.platform == "win32":
    import msvcrt
    # Binary mode is required for persistent mode on Windows.
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stderr.fileno(), os.O_BINARY)


#Splunk's Persistent REST handler class
from splunk.persistconn.application import PersistentServerConnectionApplication


class SimHandler(PersistentServerConnectionApplication):
    def __init__(self, command_line, command_arg):
        PersistentServerConnectionApplication.__init__(self)

    def handle(self, in_string):
        try:
            query_params=json.loads(in_string)
            resp = dict(query_params["query"]).get('id',"noop")
            
            return {'payload': fire_search.format(test_id=resp,dest_addr="192.169.1.1"),  # Payload of the request.
                    'status': 200          # HTTP status code
            }
        except Exception as e:
            return {'payload': str(e) ,  # Payload of the request.
                    'status': 500          # HTTP status code
            }
