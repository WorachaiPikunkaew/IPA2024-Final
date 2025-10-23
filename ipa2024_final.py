#######################################################################################
# Yourname: Worachai Pikunkaew
# Your student ID: 66070177
# Your GitHub Repo: https://github.com/WorachaiPikunkaew/IPA2024-Final

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

import time, os, requests,json, restconf_final
from dotenv import load_dotenv

#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

load_dotenv()

ACCESS_TOKEN = os.environ.get("WEBEX_ACCESS_TOKEN")

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vZmE3MjEzZTAtYWY3NS0xMWYwLWE1MTgtY2ZhNjllZTI2MTE1" # MY OWN ROOM ID, CHANGE TO REAL ROOM ID LATER
)

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

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
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

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
    if message.startswith("/66070177"):

        # extract the command
        command = message.split(" ")[1]
        print(command)

# 5. Complete the logic for each command

        if command == "create":
            responseMessage = restconf_final.create()
            print(responseMessage)

            msg_body = {
                "roomId": roomIdToGetMessages,
                "text": responseMessage
            }

            r = requests.post(
                "https://webexapis.com/v1/messages",
                data=json.dumps(msg_body),
                headers=getHTTPHeader
            )
            if not r.status_code == 200:
                raise Exception(
                    "Incorrect reply from Webex Teams API. Status code: {}, {}".format(r.status_code, r.content)
                )
        elif command == "delete":
            responseMessage = restconf_final.delete()
            print(responseMessage)

            msg_body = {
                "roomId": roomIdToGetMessages,
                "text": responseMessage
            }
            
            r = requests.post(
                "https://webexapis.com/v1/messages",
                data=json.dumps(msg_body),
                headers=getHTTPHeader
            )
            if not r.status_code == 200:
                raise Exception(
                    "Incorrect reply from Webex Teams API. Status code: {}, {}".format(r.status_code, r.content)
                )
        elif command == "enable":
            responseMessage = restconf_final.enable()
            print(responseMessage)
            msg_body = {
                "roomId": roomIdToGetMessages,
                "text": responseMessage
            }
            r = requests.post(
                "https://webexapis.com/v1/messages",
                data=json.dumps(msg_body),
                headers=getHTTPHeader
            )
            if not r.status_code == 200:
                raise Exception(
                    "Incorrect reply from Webex Teams API. Status code: {}, {}".format(r.status_code, r.content)
                )
        elif command == "disable":
            responseMessage = restconf_final.disable()
            print(responseMessage)
            msg_body = {
                "roomId": roomIdToGetMessages,
                "text": responseMessage
            }
            r = requests.post(
                "https://webexapis.com/v1/messages",
                data=json.dumps(msg_body),
                headers=getHTTPHeader
            )
            if not r.status_code == 200:
                raise Exception(
                    "Incorrect reply from Webex Teams API. Status code: {}, {}".format(r.status_code, r.content)
                )
        # elif command == "status":
        #     <!!!REPLACEME with code for status command!!!>
        #  elif command == "gigabit_status":
        #     <!!!REPLACEME with code for gigabit_status command!!!>
        # elif command == "showrun":
        #     <!!!REPLACEME with code for showrun command!!!>
        # else:
        #     responseMessage = "Error: No command or unknown command"
        
# 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        # if command == "showrun" and responseMessage == 'ok':
        #     filename = "<!!!REPLACEME with show run filename and path!!!>"
        #     fileobject = <!!!REPLACEME with open file!!!>
        #     filetype = "<!!!REPLACEME with Content-type of the file!!!>"
        #     postData = {
        #         "roomId": <!!!REPLACEME!!!>,
        #         "text": "show running config",
        #         "files": (<!!!REPLACEME!!!>, <!!!REPLACEME!!!>, <!!!REPLACEME!!!>),
        #     }
        #     postData = MultipartEncoder(<!!!REPLACEME!!!>)
        #     HTTPHeaders = {
        #     "Authorization": ACCESS_TOKEN,
        #     "Content-Type": <!!!REPLACEME with postData Content-Type!!!>,
        #     }
        # # other commands only send text, or no attached file.
        # else:
        #     postData = {"roomId": <!!!REPLACEME!!!>, "text": <!!!REPLACEME!!!>}
        #     postData = json.dumps(postData)

        #     # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        #     HTTPHeaders = {"Authorization": <!!!REPLACEME!!!>, "Content-Type": <!!!REPLACEME!!!>}   

        # # Post the call to the Webex Teams message API.
        # r = requests.post(
        #     "<!!!REPLACEME with URL of Webex Teams Messages API!!!>",
        #     data=<!!!REPLACEME!!!>,
        #     headers=<!!!REPLACEME!!!>,
        # )
        # if not r.status_code == 200:
        #     raise Exception(
        #         "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        #     )
