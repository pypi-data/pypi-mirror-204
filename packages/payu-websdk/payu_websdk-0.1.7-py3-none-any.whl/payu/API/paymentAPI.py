import sys
sys.path.append("..")

import json
from resources.hasher import APIHash
import requests

headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

def verifyPayment (creds, txnid):
    payload = {
        "key": creds["key"],
        "command": "verify_payment",
        "var1": txnid,
        "hash": ""
    }
    payload["hash"] = APIHash(creds, payload)
    response = requests.request("POST", creds["apiURL"], data=payload, headers=headers)
    return response.text


def checkPayment (creds, payuid):
    payload = {
        "key": creds["key"],
        "command": "check_payment",
        "var1": payuid,
        "hash": ""
    }
    payload["hash"] = APIHash(creds, payload)
    response = requests.request("POST", creds["apiURL"], data=payload, headers=headers)
    return response.text

def cancelRefundTransaction (creds, payuid, tokenid, amount):
    payload = {
        "key": creds["key"],
        "command": "cancel_refund_transaction",
        "var1": payuid,
        "var2": tokenid,
        "amount": amount,
        "hash": ""
    }
    payload["hash"] = APIHash(creds, payload)
    response = requests.request("POST", creds["apiURL"], data=payload, headers=headers)
    return response.text

def checkIsDomestic (creds, bin):
    payload = {
        "key": creds["key"],
        "command": "check_isDomestic",
        "var1": bin,
        "hash": ""
    }
    payload["hash"] = APIHash(creds, payload)
    response = requests.request("POST", creds["apiURL"], data=payload, headers=headers)
    return response.text

def eligibleBinsForEMI(creds, bin):
    payload = {
        "key": creds["key"],
        "command": "eligibleBinsForEMI",
        "var1": "bin",
        "var2": bin,
        "hash": ""
    }
    payload["hash"] = APIHash(creds, payload)
    response = requests.request("POST", creds["apiURL"], data=payload, headers=headers)
    return response.text



def getEmiAmountAccordingToInterest(creds, amount):
    payload = {
        "key": creds["key"],
        "command": "getEmiAmountAccordingToInterest",
        "var1": amount,
        "hash": ""
    }
    payload["hash"] = APIHash(creds, payload)
    response = requests.request("POST", creds["apiURL"], data=payload, headers=headers)
    return response.text

def getCheckoutDetails(creds, params):
    payload = {
        "key": creds["key"],
        "command": "get_checkout_details",
        "var1": json.dumps(params),
        "hash": ""
    }
    payload["hash"] = APIHash(creds, payload)
    response = requests.request("POST", creds["apiURL"], data=payload, headers=headers)
    return response.text

def getSettlementDetails(creds, dateOrUTR):
    payload = {
        "key": creds["key"],
        "command": "get_settlement_details",
        "var1": dateOrUTR,
        "hash": ""
    }
    payload["hash"] = APIHash(creds, payload)
    response = requests.request("POST", creds["apiURL"], data=payload, headers=headers)
    return response.text

def getNetbankingStatus(creds, bankcode):
    payload = {
        "key": creds["key"],
        "command": "getNetbankingStatus",
        "var1": bankcode,
        "hash": ""
    }
    payload["hash"] = APIHash(creds, payload)
    response = requests.request("POST", creds["apiURL"], data=payload, headers=headers)
    return response.text

def getIssuingBankStatus(creds, bin):
    payload = {
        "key": creds["key"],
        "command": "getIssuingBankStatus",
        "var1": bin,
        "hash": ""
    }
    payload["hash"] = APIHash(creds, payload)
    response = requests.request("POST", creds["apiURL"], data=payload, headers=headers)
    return response.text

def createInvoice(creds, params):
    payload = {
        "key": creds["key"],
        "command": "create_invoice",
        "var1": json.dumps(params),
        "hash": ""
    }
    payload["hash"] = APIHash(creds, payload)
    response = requests.request("POST", creds["apiURL"], data=payload, headers=headers)
    return response.text