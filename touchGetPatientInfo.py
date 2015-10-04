import json
import http.client
import urllib.parse
import sys

#url for the ga

import touchworksinit as touch

uc = touch.init()
print("UC=", uc)

PARAMS = {}

PATIENT = {}

PATIENT['firstname'] = 'Alannah'

PATIENT['lastname'] = 'De Bernales'
PATIENT['search'] = 'De*,Al*'

def getPatientInfo(uc, pt):
    touch.initParams(PARAMS)
    action = 'SearchPatients'
    print (pt)
    #PARAMS[1] = '*' + pt['lastname'] + '*'
    #PARAMS[1] = pt['firstname']
    PARAMS[1]  = pt['lastname']
    PARAMS[1] = pt['search']
    #PARAMS[1] = 'De*,Al*'

    jsonstr = touch.buildjson(action, uc, PARAMS, '')
    uout = touch.unityaction(uc, jsonstr)
    touch.uoutPrint(action, uout)

getPatientInfo(uc, PATIENT)


def getPatientByMRN(uc):

    touch.initParams(PARAMS)
    action = 'GetPatientByMRN'
    PARAMS[1] = '12345678'


