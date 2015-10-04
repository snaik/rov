import json
import http.client
import urllib.parse
import sys

#url for the ga

#Start of Initialization
UC = {}

UC['url'] = 'http://twlatestga.unitysandbox.com'
UC['svc_user'] = 'DocAm-0603-RapidOpiat-test'
UC['svc_pass'] = 'D!2@9pR@p0daP#9T%vf%w0rt%stdpp'

UC['Appname'] = 'DocAmp.RapidOpiateViewer.TestApp'


UC['ehr_user'] = 'jmedici'
UC['ehr_pass'] = 'password01'
UC['security_token'] = ''
PARAMS = {}

def initParams(params):
    params[0] = ''
    params[1] = ''
    params[2] = ''
    params[3] = ''
    params[4] = ''
    params[5] = ''
    params[6] = ''

# build Magic action JSON string
def buildjson(action, uc, params, data=''):
    return json.dumps({'Action': action,
                       'Appname': uc['Appname'],
                       'AppUserID': uc['ehr_user'],
                       'PatientID': params[0],
                       'Token': uc['security_token'],
                       'Parameter1': params[1],
                       'Parameter2': params[2],
                       'Parameter3': params[3],
                       'Parameter4': params[4],
                       'Parameter5': params[5],
                       'Parameter6': params[6],
                       'Data': data})


# get Unity security token from GetToken endpoint
def gettoken(uc):

    u = urllib.parse.urlparse(uc['url'])

    if (u.scheme == 'http'):
        conn = http.client.HTTPConnection(u.hostname)
    elif (u.scheme == 'https'):
        conn = http.client.HTTPSConnection(u.hostname)

    conn.request('POST',
                 '/Unity/UnityService.svc/json/GetToken',
             json.dumps({'Username': uc['svc_user'],
                         'Password': uc['svc_pass']}),
             {'Content-Type': 'application/json'})

    response = conn.getresponse( )
    t = response.read( ).decode( )
    conn.close( )
    return t


# post action JSON to MagicJson endpoint, get JSON in return
def unityaction(uc, jsonstr):
    u = urllib.parse.urlparse(uc['url'])
    if (u.scheme == 'http'):
        conn = http.client.HTTPConnection(u.hostname)
    elif (u.scheme == 'https'):
        conn = http.client.HTTPSConnection(u.hostname)

    conn.request('POST',
                 '/Unity/UnityService.svc/json/MagicJson',
             jsonstr,
             {'Content-Type': 'application/json'})
    resp = conn.getresponse( )
    retjson = resp.read( ).decode( )
    conn.close( )
    return retjson


# Get Unity security token
def getSecurityToken(uc):
    #Get the url
    u = urllib.parse.urlparse(uc['url'])
    conn = http.client.HTTPConnection(u.hostname)
    if (u.scheme == 'https'):
        conn = http.client.HTTPSConnection(u.hostname)

    conn.request('POST',
                 '/Unity/UnityService.svc/json/GetToken',
                json.dumps({'Username': uc['svc_user'],
                         'Password': uc['svc_pass']}),
             {'Content-Type': 'application/json'})

    response = conn.getresponse( )
    t = response.read( ).decode( )
    conn.close( )
    uc['security_token'] = t
    print('Using Unity security token: ' + uc['security_token'])


def uoutPrint(action, uout):
    print('Output from ', action)
    print(json.dumps(json.loads(uout), indent=4, separators=(',', ': ')))

def authenticateEHR(uc):
   # Authenticate EHR user before calling other Magic actions
    initParams(PARAMS)
    PARAMS[1] = uc['ehr_pass']
    jsonstr = buildjson('GetUserAuthentication', uc, PARAMS)

    print (jsonstr)
    unity_output = unityaction(uc, jsonstr)

    print('Output from GetUserAuthentication: ')
    print(json.dumps(json.loads(unity_output), indent=4, separators=(',', ': ')))
    print( )

    # Look for ValidUser = YES
    json_dict = json.loads(unity_output)
    valid_user = json_dict[0]['getuserauthenticationinfo'][0]['ValidUser']
    if (valid_user == 'YES'):
	    print('EHR user is valid.')
    else:
    	print('EHR user is invalid: ' + json_dict[0]['getuserauthenticationinfo'][0]['ErrorMessage'])
    print( )


def getServerInfo(uc):
    # Call GetServerInfo Magic action; patient ID, Parameter1-6, and data not used
    initParams(PARAMS)
    jsonstr = buildjson('GetServerInfo', uc, PARAMS, '')
    unity_output = unityaction(uc, jsonstr)

    print('Output from GetServerInfo: ')
    print(json.dumps(json.loads(unity_output), indent=4, separators=(',', ': ')))

def initUnity(uc):
    getSecurityToken(uc)
    authenticateEHR(uc)
    getServerInfo(uc)
    return uc

def init():
    return initUnity(UC)
