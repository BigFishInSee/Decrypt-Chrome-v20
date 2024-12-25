import requests
import websocket
import json
import subprocess
import os

dbPort = 9222
dp_url = f'http://localhost:{dbPort}/json'
path = rf"C:\Program Files\Google\Chrome\Application\chrome.exe"
appData = os.getenv('LOCALAPPDATA')
userDataDirectory = rf'{appData}\google\chrome\User Data'

def getDebugWsURL():
    res = requests.get(dp_url)
    data = res.json()
    return data[0]['webSocketDebuggerUrl'].strip()

def killCrhome():
    subprocess.run('taskkill /F /IM chrome.exe', check=False, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def startDebug():
    subprocess.Popen([
    path,
    f'--remote-debugging-port={dbPort}',
    '--remote-allow-origins=*',
    '--profile-directory=Default',  
    f'--user-data-dir={userDataDirectory}'
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
def save_cookies(cookies, filename="cookies.json"):
    """Save cookies to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(cookies, f, indent=4)
    print(f"Cookies have been saved to {filename}")

if __name__ == "__main__":
    killCrhome()
    startDebug()
    url = getDebugWsURL()
    ws = websocket.create_connection(url)
    ws.send(json.dumps({'id': 1, 'method': 'Network.getAllCookies'}))
    response = ws.recv()
    response = json.loads(response)
    cookies = response['result']['cookies']
    save_cookies(cookies)
    print(json.dumps(cookies, indent=4))
    ws.close()
    killCrhome()
