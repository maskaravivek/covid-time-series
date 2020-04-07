import requests
from datetime import datetime

URL = "https://commons.wikimedia.org/w/api.php"

def get_credentials():
    f = open("credentials.txt", "r")
    credentials = f.read()
    creds = credentials.split(',')
    return creds[0], creds[1]

def summary(description):
    f = open("summary.txt", "r")
    summary_text = f.read()
    summary = summary_text.replace('descText', description).replace(
        'dateTime', str(datetime.today()))
    return summary

def login():
    S = requests.Session()

    # Step 1: Retrieve a login token
    PARAMS_1 = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_1)
    DATA = R.json()

    LOGIN_TOKEN = DATA["query"]["tokens"]["logintoken"]

    username, password = get_credentials()

    # Step 2: Send a post request to login. Use of main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
    PARAMS_2 = {
        "action": "login",
        "lgname": username,
        "lgpassword": password,
        "format": "json",
        "lgtoken": LOGIN_TOKEN
    }

    R = S.post(URL, data=PARAMS_2)
    return S

def upload(S, dir, fileName, description):
    FILE_PATH = 'plots/'+dir+'/' + fileName
    # Step 3: Obtain a CSRF token
    PARAMS_3 = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_3)
    DATA = R.json()

    CSRF_TOKEN = DATA["query"]["tokens"]["csrftoken"]

    summary_text = summary(description)
    # Step 4: Post request to upload a file directly
    PARAMS_4 = {
        "action": "upload",
        "filename": fileName,
        "text": summary_text,
        "format": "json",
        "token": CSRF_TOKEN,
        "ignorewarnings": 1
    }

    FILE = {'file': (fileName,
                     open(FILE_PATH, 'rb'), 'multipart/form-data')}

    R = S.post(URL, files=FILE, data=PARAMS_4)
    print(R)
    DATA = R.json()
    print(DATA)
