'''
Created on 13 sept. 2019

@author: WUIAPE03
'''
import requests
import json


#text = '<p align=\"center\">Chat Started: Wednesday, September 11, 2019, 23:37:03 (+0000)</p><p align=\"center\">Chat Origin: brainapi buttons</p><p align=\"center\">Agent Aday P</p>( 8s ) Aday P: Welcome to Brainapi Chat!<br>( 23s ) Visitor: Ok<br>( 35s ) Aday P: Funciona!!!<br>( 1m 31s ) Aday P: desde Python<br>( 1m 38s ) Visitor: chachi<br>',
text = 'Funciona'

def salesforce_Autentication():
    url = 'https://login.salesforce.com/services/oauth2/token'
    client_id = '3MVG9Ve.2wqUVx_Y8TNEQX1d87g2oyIvSc1orA7Z0AXA53wWMatRS9Qiuq8k3Y.2e8DpgmHlQVMVj86F5ZfXJ'
    client_secret = '1BEB67C7F1FBF9626D7FA75A4B557698C8687B802F6E68D06D7A581821D9E15A'
    grant_type = 'password'
    username = 'adaypr@gmail.com'
    password = 'Indira_83'
    
    params = {'client_id': client_id,
              'client_secret' : client_secret,
              'grant_type': grant_type,
              'username': username,
              'password' : password }
    
    r = requests.post(url, params=params)
    return json.loads(r.text)['access_token']

def salesforce_LiveChatTranscript(text, leadPhone,  authtoken):
    url = 'https://eu25.salesforce.com/services/apexrest/LiveChatTranscript/'
    
    data = {
    'AverageResponseTimeOperator': '0',
    'AverageResponseTimeVisitor': '0',
    'Body': text,
    'Browser': 'Chrome 76.0.3809.132',
    'BrowserLanguage': 'es-ES',
    'EndedBy': 'Visitor',
    'IpAddress': '37.252.182.47',
    'Location': 'Las Palmas de G.C.',
    'MaxResponseTimeOperator': '11',
    'MaxResponseTimeVisitor': '15',
    'OperatorMessageCount': '3',
    'OwnerId': '0052o000008yN8RAAU',
    'Platform': 'Win10',
    'ScreenResolution': '1366x768',
    'Status': 'Completed',
    'UserAgent': 'Chatbot',
    'VisitorMessageCount': '2',
    'VisitorNetwork': 'Elephant Talk Network Systems',
    'leadPhone': leadPhone
    }
    
    hed = {'Authorization': 'Bearer ' + authtoken}
    r = requests.post(url, json=data, headers=hed)
    return json.loads(r.text)


