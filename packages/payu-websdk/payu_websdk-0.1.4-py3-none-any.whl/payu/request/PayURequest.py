import sys
sys.path.append("..")

from resources.hasher import generate_hash
from typing import Dict

def generate_payment_form(creds: Dict[str, str], params: Dict[str, str]) -> str:
    mandatory_params = ["txnid", "amount", "productinfo", "firstname", "email", "phone", "surl", "furl"]
    for param_name in mandatory_params:
        if param_name not in params:
            raise ValueError(f"Missing mandatory parameter '{param_name}'")
    params["hash"] = generate_hash(creds, params)
    params["key"] = creds["key"]
    form = "<form name=\"payment_post\" id=\"payment_post\" action=\"" + creds["paymentURL"] + "\" method=\"post\">"
    for key, value in params.items():
        form += f"<input hidden type=\"text\" name=\"{key}\" value=\"{value}\"/>"
    form += "</form><script type=\"text/javascript\"> window.onload=function(){document.forms['payment_post'].submit();}</script>"
    return form
        

         
        









