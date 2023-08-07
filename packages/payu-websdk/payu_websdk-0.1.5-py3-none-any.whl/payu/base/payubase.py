class Base(object):
    _instance = None
    key = ""
    salt = ""
    paymentURL = ""
    apiURL = ""

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Base, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def set_params(self,params):
        self.key = params.get("key")
        self.salt = params.get("salt")
        self.env = params.get("env")
        self.paymentURL = params.get("paymentURL")
        self.apiURL = params.get("apiURL")
        return (self.key ,self.salt, self.paymentURL, self.apiURL) 

    def get_params(self):
        return ({
            "key": self.key,
            "salt":self.salt,
            "paymentURL":self.paymentURL,
            "apiURL": self.apiURL
        })


