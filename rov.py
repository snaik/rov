import json
import http.client
import urllib.parse
import sys

#url for the ga


urlga = 'http://twlatestga.unitysandbox.com'

Svc_username = 'DocAm-0603-RapidOpiat-test'
Svc_password = 'D!2@9pR@p0daP#9T%vf%w0rt%stdpp'
Appname      = 'DocAmp.RapidOpiateViewer.TestApp'
Ehr_username = 'jmedici'
Ehr_password = 'password01'


# build Magic action JSON string
def buildjson(action, appname, ehruserid, patientid, unitytoken,
              param1='', param2='', param3='', param4='', param5='', param6='', data=''):
    return json.dumps({'Action': action,
                       'Appname': appname,
                       'AppUserID': ehruserid,
                       'PatientID': patientid,
                       'Token': unitytoken,
                       'Parameter1': param1, 'Parameter2': param2, 'Parameter3': param3,
                       'Parameter4': param4, 'Parameter5': param5, 'Parameter6': param6,
                       'Data': data})


# get Unity security token from GetToken endpoint
def gettoken(username, password):
    u = urllib.parse.urlparse(urlga)
    
    if (u.scheme == 'http'):
        conn = http.client.HTTPConnection(u.hostname)
    elif (u.scheme == 'https'):
        conn = http.client.HTTPSConnection(u.hostname)
    
    conn.request('POST', '/Unity/UnityService.svc/json/GetToken',
             json.dumps({'Username': username, 'Password': password}),
             {'Content-Type': 'application/json'})
    response = conn.getresponse( )
    t = response.read( ).decode( )
    conn.close( )
    return t


# post action JSON to MagicJson endpoint, get JSON in return
def unityaction(jsonstr):
    u = urllib.parse.urlparse(urlga)
    
    if (u.scheme == 'http'):
        conn = http.client.HTTPConnection(u.hostname)
    elif (u.scheme == 'https'):
        conn = http.client.HTTPSConnection(u.hostname)

    conn.request('POST', '/Unity/UnityService.svc/json/MagicJson',
             jsonstr,
             {'Content-Type': 'application/json'})
    resp = conn.getresponse( )
    retjson = resp.read( ).decode( )
    conn.close( )
    return retjson


# Get Unity security token
token = gettoken(Svc_username, Svc_password)
print('Using Unity security token: ' + token)

# Authenticate EHR user before calling other Magic actions
jsonstr = buildjson('GetUserAuthentication', Appname, Ehr_username, '', token, Ehr_password)
unity_output = unityaction(jsonstr)

# Uncomment to display full GetUserAuthentication output
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

# Call GetServerInfo Magic action; patient ID, Parameter1-6, and data not used
jsonstr = buildjson('GetServerInfo', Appname, Ehr_username, '', token)
unity_output = unityaction(jsonstr)

print('Output from GetServerInfo: ')
print(json.dumps(json.loads(unity_output), indent=4, separators=(',', ': ')))

ShowWand = 'Y'

# Call GetServerInfo Magic action; patient ID, Parameter1-6, and data not used
jsonstr = buildjson('LastLogs', Appname, Ehr_username, '', token, '', 'Y', 10)
unity_output = unityaction(jsonstr)

print('Output from LastLogs: ')
print(json.dumps(json.loads(unity_output), indent=4, separators=(',', ': ')))

# Call GetServerInfo Magic action; patient ID, Parameter1-6, and data not used
jsonstr = buildjson('GetClinicalSummary', Appname, Ehr_username, 889, token, 'Medications|Vitals', '', 'Y')
unity_output = unityaction(jsonstr)
print(json.dumps(json.loads(unity_output), indent=4, separators=(',', ': ')))

jsonstr = buildjson('GetMedicationInfo', Appname, Ehr_username, '', token, 66149)
unity_output = unityaction(jsonstr)
print(json.dumps(json.loads(unity_output), indent=4, separators=(',', ': ')))



