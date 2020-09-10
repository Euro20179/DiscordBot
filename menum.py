class enum(dict):
    def __init__(self, *properties, **kwargs):
        self.___PROPS = properties
        self.___KWARGS = {v: k for k, v in kwargs.items()}
        self.___LEN = len(properties) + len(kwargs.values())
        self.___KWARPROPS = {}
        for n, prop in enumerate(properties):
            self.__dict__[prop] = n
            self.___KWARPROPS[prop] = n
        for k, v in kwargs.items():
            self.__dict__[k] = v
        super().__init__(**{k: v for k, v in self.__dict__.items() if k[0:8] != "_enum___"})

    def getByValue(self, value):
        for k, v in self.items():
            if v == value:
                return k
        return None
        
    def __len__(self):
        return self.___LEN

    def __str__(self):
        return f'{self.___PROPS} {self.___KWARGS}'.replace("{}", "").strip()