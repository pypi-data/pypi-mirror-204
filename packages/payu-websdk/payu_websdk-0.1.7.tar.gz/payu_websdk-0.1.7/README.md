# PayU SDK for Python Apis
This API gives you the status of the transaction. PayU recommends this API to reconcile with PayU’s database after you receive the response, where var1 is your transaction id.

## Features Supported
Following features are supported in the PayU Python web SDK:
- Create Payment Link.
- Verify transactions, check the transaction status, transaction details, or discount rate for a transaction
- Initiated refunds, cancel refund, check refund status.
- Retrieve settlement details which the bank has to settle you.
- Get information of the payment options, offers, recommendations, and downtime details.
- Check the customer’s eligibility for EMI and get the EMI amount according to interest
- Pay by link
  To get started with PayU, visit our [Developer Guide](https://devguide.payu.in/low-code-web-sdk/getting-started-low-code-web-sdk/register-for-a-test-merchant-account/)
# Table of Contents
    
1. [Installation](#usage)
2. [Getting Started](#getting-started)
3. [Documentation for various Methods](#documentation-for-various-methods)
## Usage
```shell
pip install payu_websdk
```
## Getting Started


```shell

client = payu_websdk.payUClient(<KEY>,<SALT>,<ENV>) // Need to set merchant key,salt and env ("TEST"/"LIVE")

```