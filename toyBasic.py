class BasLangError(Exception):
    def __init__(self, msg):
        self.message = msg

class BasTypeError(BasLangError):
    def __init__(self, msg):
        super().__init__(msg)

class BasLangValue:
    def __init__(self, init_value=0.0, init_type="number"):
        self.type = init_type
        if init_type == "number":
            self.value = float(init_value)
        else:
            self.value = init_value

    def __str__(self) -> str:
        return str(self.value)
    
    def add(self, other: 'BasLangValue') -> 'BasLangValue':
        if self.type == "number":
            if other.type != "number":
                raise BasTypeError("cannot add " + str(other.value) + " to a number")
            return BasLangValue(init_value=self.value+other.value)
        elif self.type == "string":
            return BasLangValue(init_type="string", init_value=self.value+str(other.value))
    
    def sub(self, other: 'BasLangValue') -> 'BasLangValue':
        if self.type != "number":
            raise BasTypeError("cannot subtract from type " + self.type)
        elif other.type != "number":
            raise BasTypeError("cannot subtract " + other.type + " from a number")
        return BasLangValue(init_value=self.value-other.value)
    
    def mul(self, other: 'BasLangValue') -> 'BasLangValue':
        if self.type == "number":
            if other.type != "number":
                raise BasTypeError("cannot multiply " + str(other.value) + " by a number")
            return BasLangValue(init_value=self.value*other.value)
        elif self.type == "string":
            raise BasTypeError("cannot multiply a string")
    
    def div(self, other: 'BasLangValue') -> 'BasLangValue':
        if self.type == "number":
            if other.type != "number":
                raise BasTypeError("cannot divide " + str(other.value) + " by a number")
            return BasLangValue(init_value=self.value/other.value)
        elif self.type == "string":
            raise BasTypeError("cannot divide a string")
    
    
    def compare(self, other: 'BasLangValue') -> str:
        if self.type != other.type:
            raise BasTypeError("cannot compare " + self.type + " to " + other.type)
        elif self.value < other.value:
            return "less"
        elif self.value == other.value:
            return "equal"
        else:
            return "greater"
    

    
