from base.payubase import Base
from request.PayURequest import generate_payment_form
from API.paymentAPI import *
from resources.hasher import *

class payUClient:
    paymentURL = ""
    apiURL = ""
    def __init__(self, key, salt, env):
        if len(key) == 0:
            raise ValueError("Invalid input. Empty string passed in the key param")
        if len(salt) == 0:
            raise ValueError("Invalid input. Empty string passed in the salt param")
        if(env == "TEST"):
            self.paymentURL = "https://test.payu.in/_payment"
            self.apiURL = "https://test.payu.in/merchant/postservice.php?form=2"
        elif(env == "LIVE"):
            self.paymentURL = "https://secure.payu.in/_payment"
            self.apiURL = "https://info.payu.in/merchant/postservice.php?form=2"
        else:
            raise ValueError("Invalid input. Pleas enter the correct environment, possible values can be 'TEST' or 'LIVE'")
        Base().set_params({
            "key": key,
            "salt": salt,
            "paymentURL": self.paymentURL,
            "apiURL": self.apiURL
        })

    def generatePaymentForm(self, params):
        return generate_payment_form(Base().get_params(), params)
    
    def verifyPayment(self, txnid):
        return verifyPayment(Base().get_params(),txnid)
    
    def checkPayment(self, payuid):
        return checkPayment(Base().get_params(),payuid)
    
    def cancelRefundTransaction(self, payuid, tokenid, amount):
        return cancelRefundTransaction(Base().get_params(),payuid, tokenid, amount)
    
    def checkIsDomestic(self, bin):
        return checkIsDomestic(Base().get_params(),bin)
    
    def eligibleBinsForEMI(self,bin):
        return eligibleBinsForEMI(Base().get_params(),bin)
    
    def getEmiAmountAccordingToInterest(self, amount):
        return getEmiAmountAccordingToInterest(Base().get_params(), amount)
    
    def getCheckoutDetails(self, params):
        return getCheckoutDetails(Base().get_params(), params)
    
    def getSettlementDetails(self, dateOrUTR):
        return getSettlementDetails(Base().get_params(), dateOrUTR)
    
    def getNetbankingStatus(self, bankcode):
        return getNetbankingStatus(Base().get_params(), bankcode)
    
    def getIssuingBankStatus(self, bin):
        return getIssuingBankStatus(Base().get_params(), bin)
    
    def createInvoice(self, params):
        return createInvoice(Base().get_params(), params)
    
    def generatePaymentHash(self, params):
        return generate_hash(Base().get_params(),params)
    
    def generateReverseHash(self, params):
        return generate_reverse_hash(Base().get_params(),params)
    
    def validateReverseHash(self, params):
        return validate_hash(Base().get_params(),params)