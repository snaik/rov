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

    #Retrive the patient id
    parsed_json = json.loads(uout)
    pinfo = parsed_json[0]['searchpatientsinfo']
    ID = pinfo[0]['ID']
    PATIENT['ID'] = ID


def getClinicalSummary(uc, pt):
    touch.initParams(PARAMS)
    action = 'GetClinicalSummary'
    PARAMS[0] = PATIENT['ID']
    PARAMS[1] = 'Medications'
    PARAMS[2] = '' #Encounter
    PARAMS[3] = 'Y'

    jsonstr = touch.buildjson(action, uc, PARAMS, '')
    uout = touch.unityaction(uc, jsonstr)
    touch.uoutPrint(action, uout)

    #Retrieve the GetClinical Summary
    parsed_json = json.loads(uout)
    cinfo = parsed_json[0]['getclinicalsummaryinfo']

    totalRx = len(cinfo)
    medAttrib = { 'transid',  'code', 'entrycode', 'status',  'displaydate', 'description', 'detail' }
    for i in range(0, totalRx):
        rx = cinfo[i]
        print( "%10s %-8s %-8s %-10s %-10s %-40.40s === [%-40s]" % (
            rx['transid'],
            rx['code'],
            rx['entrycode'],
            rx['status'],
            rx['displaydate'],
            rx['description'],
            rx['detail']
        ))

        meds = ""
        meds = rx['transid']
        meds = meds + " " + rx['code']
        meds = meds + " " + rx['entrycode']
        meds = meds + " " + rx['status']
        meds = meds + " " + rx['displaydate']
        meds = meds + " " + rx['description']
        meds = meds + " " + rx['detail']
        #print (meds)

    return
    medications = ""
    for attr in medAttrib:
        medications = medications + " " + c0[attr]
        #print(attr)
        
    print("%s" % (medications))
        
    #print("cinfo=", cinfo)
    
getPatientInfo(uc, PATIENT)
getClinicalSummary(uc, PATIENT)





def getPatientByMRN(uc):

    touch.initParams(PARAMS)
    action = 'GetPatientByMRN'
    PARAMS[1] = '12345678'


