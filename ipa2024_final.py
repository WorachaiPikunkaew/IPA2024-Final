#######################################################################################
# Yourname: Worachai Pikunkaew
# Your student ID: 66070177
# Your GitHub Repo: https://github.com/WorachaiPikunkaew/IPA2024-Final

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

import time, os, requests, json
import restconf_final, netconf_final, netmiko_final, ansible_final
from requests_toolbelt import MultipartEncoder
from dotenv import load_dotenv

#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

load_dotenv()# load environment variables from a .env file
ACCESS_TOKEN = os.environ.get("WEBEX_ACCESS_TOKEN")

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
ROOM_ID = (
   "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vYmQwODczMTAtNmMyNi0xMWYwLWE1MWMtNzkzZDM2ZjZjM2Zm" # IPA2025 Room ID
)

def msg_send(responseMessage):
    print("Sending message:", responseMessage)
    msg_body = {"roomId": ROOM_ID, "text": responseMessage}
    r = requests.post(
        "https://webexapis.com/v1/messages",
        data = json.dumps(msg_body),
        headers = {"Authorization": "Bearer "+ACCESS_TOKEN,  "Content-Type": "application/json"}
    )
    print("Message sent, content:", r.content)
    if not r.status_code == 200:
        raise Exception("Incorrect reply from Webex Teams API. Status code: {}, {}".format(r.status_code, r.content))
    
def is_valid_ip(ip: str) -> bool:
    octevs = ip.split(".")
    if len(octevs) != 4:
        return False
    for octave in octevs:
        if not octave.isdigit() or not 0 <= int(octave) <= 255:
            return False
    return True

conf_method = "" # variable to hold user selected configuration method: restconf or netconf
while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": ROOM_ID, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": "Bearer "+ACCESS_TOKEN,
                     "Content-Type": "application/json"}

    # 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception("Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code))

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    ipv4_address = ""
    if message.startswith("/66070177 "):
        command_list = message.split(" ")[1:] # ignore the first part which is /studentID
        if command_list[0] in ["netconf", "restconf"]: # check for user selected method
            conf_method = command_list[0]
            print("Selected method: {}".format(conf_method))
            msg_send("Ok: {}".format(conf_method.capitalize()))
            continue
        elif not conf_method: # if no method selected yet and command is not to select method
            print("No method selected yet")
            msg_send("Error: No method specified")
            continue
        else:
            ipv4_address = command_list[0]
            if not is_valid_ip(ipv4_address):
                print("Invalid IPv4 address: {}".format(ipv4_address))
                msg_send("Error: No IP specified")
                continue
            restconf_final.set_ip(ipv4_address)
            netconf_final.set_ip(ipv4_address)
            print("Using method: {}".format(conf_method))
            print("Using IPv4 address: {}".format(ipv4_address))

        command = command_list[-1] # last argument should be the command
        # only process further if a method has been selected
        


    # 5. Complete the logic for each command
        commandResponse = ""
        if command == "create":
            commandResponse = restconf_final.create() if conf_method == "restconf" else netconf_final.create()
        elif command == "delete":
            commandResponse = restconf_final.delete() if conf_method == "restconf" else netconf_final.delete()
        elif command == "enable":
            commandResponse = restconf_final.enable() if conf_method == "restconf" else netconf_final.enable()
        elif command == "disable":
            commandResponse = restconf_final.disable() if conf_method == "restconf" else netconf_final.disable()
        elif command == "status":
            commandResponse = restconf_final.status()  if conf_method == "restconf" else netconf_final.status()
        elif command == "gigabit_status":
            commandResponse = netmiko_final.gigabit_status()
        elif command == "showrun":
            commandResponse = ansible_final.showrun()
        else:
            commandResponse = "Error: No command or unknown command"
        print(command, "response with", commandResponse)
        msg_send(commandResponse)
        
        # 6. Complete the code to post the message to the Webex Teams room.

        #         The Webex Teams POST JSON data for command showrun
        #         - "roomId" is is ID of the selected room
        #         - "text": is always "show running config"
        #         - "files": is a tuple of filename, fileobject, and filetype.

        #         the Webex Teams HTTP headers, including the Authoriztion and Content-Type
                
        #         Prepare postData and HTTPHeaders for command showrun
        #         Need to attach file if responseMessage is 'ok'; 
        #         Read Send a Message with Attachments Local File Attachments
        #         https://developer.webex.com/docs/basics for more detail

        if command == "showrun" and commandResponse == 'ok':
            filename = "show_run_66070177_CSR1KV.txt"
            fileobject = open(filename, "rb")
            filetype = "text/plain"
            postData = {
                "roomId": ROOM_ID,
                "text": "show running config",
                "files": (filename, fileobject, filetype),
            }
            postData = MultipartEncoder(fields=postData)
            print("postData:", postData)
            HTTPHeaders = {
            "Authorization": "Bearer "+ACCESS_TOKEN,
            "Content-Type": postData.content_type,
            }
            r = requests.post(
                "https://webexapis.com/v1/messages",
                data=postData,
                headers=HTTPHeaders,
            )
            if not r.status_code == 200:
                raise Exception(
                    "Incorrect reply from Webex Teams API. Status code: {}: {}".format(r.status_code, r.content)
                )

        # other commands only send text, or no attached file.
        elif command == "showrun" and commandResponse != 'ok':
            msg_send(commandResponse)
