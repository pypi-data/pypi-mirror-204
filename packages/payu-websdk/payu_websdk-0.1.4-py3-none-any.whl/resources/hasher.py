import hashlib

def generate_hash(credes,params):
    key = credes.get('key')
    salt = credes.get('salt')
    txnid = params.get("txnid")
    amount = params.get("amount")
    productinfo = params.get("productinfo", "")
    firstname = params.get("firstname", "")
    email = params.get("email", "")
    udf1 = params.get("udf1", "")
    udf2 = params.get("udf2", "")
    udf3 = params.get("udf3", "")
    udf4 = params.get("udf4", "")
    udf5 = params.get("udf5", "")
    if params.get("additional_charges") is not None and params.get("additional_charges") != "":
        additional_charges = params.get("additional_charges")
        payment_hash_sequence = f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|{udf1}|{udf2}|{udf3}|{udf4}|{udf5}||||||{salt}|{additional_charges}"
    else:
        payment_hash_sequence = f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|{udf1}|{udf2}|{udf3}|{udf4}|{udf5}||||||{salt}"
    hash_value = hashlib.sha512((payment_hash_sequence).encode('utf-8')).hexdigest()
    return hash_value

def generate_reverse_hash(credes, params):
    key = credes['key']
    salt = credes['salt']
    txnid = params.get("txnid")
    amount = params.get("amount")
    productinfo = params.get("productinfo")
    firstname = params.get("firstname")
    email = params.get("email")
    udf1 = params.get("udf1", "")
    udf2 = params.get("udf2", "")
    udf3 = params.get("udf3", "")
    udf4 = params.get("udf4", "")
    udf5 = params.get("udf5", "")
    status = params.get("status")
    if params.get("additionalCharges") is not None and params.get("additionalCharges") != "":
        additional_charges = params.get("additionalCharges")
        validate_hash_sequence = f"{additional_charges}|{salt}|{status}||||||{udf5}|{udf4}|{udf3}|{udf2}|{udf1}|{email}|{firstname}|{productinfo}|{amount}|{txnid}|{key}"
    else:
        validate_hash_sequence = f"{salt}|{status}||||||{udf5}|{udf4}|{udf3}|{udf2}|{udf1}|{email}|{firstname}|{productinfo}|{amount}|{txnid}|{key}"
    validate_hash = hashlib.sha512((validate_hash_sequence).encode('utf-8')).hexdigest().lower()
    return validate_hash

def validate_hash(creds, params) -> bool:
    if (generate_reverse_hash(creds,params) == params["hash"]):
        return True
    return False

def APIHash(credes, params):
    key = credes['key']
    salt = credes['salt']
    command = params.get("command")
    var1 = params.get("var1")
    hash_sequence = f"{key}|{command}|{var1}|{salt}"
    hash_value = hashlib.sha512((hash_sequence).encode('utf-8')).hexdigest().lower()
    return hash_value

