from netmiko import ConnectHandler
from pprint import pprint

def set_ip(ip_address):
    global device_params
    device_params = {
    "device_type": "cisco_xe",
    "ip": ip_address,
    "username": username,
    "password": password,
    }
username = "admin"
password = "cisco"

# device_params = {
#     "device_type": "cisco_xe",
#     "ip": device_ip,
#     "username": username,
#     "password": password,
# }


def gigabit_status():
    ans = "default answer"
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("show ip int", use_textfsm=True)
        print("cmd_result\n",result, type(result))
        for status in result:
            print("status:", status)
            if status['interface'].startswith('GigabitEthernet'):
                ans += status['interface'] +" "+ status['link_status']
                if status['link_status'] == "up":
                    up += 1
                elif status['link_status'] == "down":
                    down += 1
                elif status['link_status'] == "administratively down":
                    admin_down += 1
            else:
                continue
            ans += ", "
        ans = ans[:-2]
        ans += " -> {} up, {} down, {} administratively down (Checked by netmiko)".format(up, down, admin_down)
        pprint(ans)
        return ans

def get_motd():
    ans = "default answer"
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_command("sh run | include banner motd", use_textfsm=True)
        print("raw motd\n",result, type(result))
        ans = result.replace("banner motd ^C", "").replace("^C", "").strip()
        pprint(ans)
        return ans