import subprocess

def showrun():
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['wsl', 'ansible-playbook', 'backup_playbook.yaml', '-i', 'inventory.ini']
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    if 'ok=2' in result:
        return "ok"
    else:
        return 'Error: Ansible'
