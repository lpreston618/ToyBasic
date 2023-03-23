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
        if self.type == other.type:
            self.value += other.value
        else:
            raise BasTypeError(f"cannot add {other.type} to {self.type}")

    def sub(self, other: 'BasLangValue') -> 'BasLangValue':
        if self.type == other.type == "number":
            self.value -= other.value
        else:
            raise BasTypeError(f"cannot subtract {other.type} from {self.type}")
        
    
    def mul(self, other: 'BasLangValue') -> 'BasLangValue':
        if self.type == other.type == "number":
            self.value *= other.value
        else:
            raise BasTypeError(f"cannot multiply {self.type} by {other.type}")
    
    def div(self, other: 'BasLangValue') -> 'BasLangValue':
        if self.type == other.type == "number":
            self.value /= other.value
        else:
            raise BasTypeError(f"cannot divide {self.type} by {other.type}")
    
    # def compare(self, other: 'BasLangValue', op: str) -> bool:
    def compare(self, other: 'BasLangValue') -> str:
        if self.type != other.type:
            raise BasTypeError("cannot compare " + self.type + " to " + other.type)
        elif self.value < other.value:
            return "less"
        elif self.value == other.value:
            return "equal"
        else:
            return "greater"

        # if op == "=":
        #     return self.value == other.value
        # elif op == "<=":
        #     return self.value <= other.value
        # elif op == ">=":
        #     return self.value >= other.value
        # elif op == "<":
        #     return self.value < other.value
        # elif op == ">":
        #     return self.value > other.value
        # elif op == "!=":
        #     return self.value != other.value
    

    
