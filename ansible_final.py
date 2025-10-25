import subprocess

def showrun(ip_address: str):
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['wsl', 'ansible-playbook', 'backup_playbook.yaml', '-i', 'inventory.ini', '--limit', ip_address]
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    if 'ok=2' in result:
        return "ok"
    else:
        return 'Error: Ansible'
def motd(ip_address: str, motd_message: str):
    command = ['wsl', 'ansible-playbook', 'motd_playbook.yaml', '-i', 'inventory.ini', '--extra-vars', f'motd_message="{motd_message}"', '--limit', ip_address]
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    if 'ok=1' in result:
        return "Ok: success"
    else:
        print("Ansible motd command result:\n", result)
        return 'Error: Ansible'
