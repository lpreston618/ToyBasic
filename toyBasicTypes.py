#####
# Contains type definitions for toyBASIC
#####

# general error wrapper for when anything goes wrong in the language
class BasLangError(Exception):
    def __init__(self, msg):
        self.message = msg

# a more specific error for cathing type mismatches
class BasTypeError(BasLangError):
    def __init__(self, msg):
        super().__init__(f"(type error) {msg}")


# a wrapper class for BASIC types. Right now, a BASIC value can only be
# either a string or a number. this class defines operations on those types
# and has some simple type checking
class BasLangValue:
    def __init__(self, init_value=0.0, init_type="number"):
        self.type = init_type
        if init_type == "number":
            self.value = float(init_value)
        else:
            self.value = init_value

    def __str__(self) -> str:
        return str(self.value)
    
    # you can add a string to a string or a number to a number,
    # but you can't add a string to a number.
    def add(self, other: 'BasLangValue') -> 'BasLangValue':
        if self.type == other.type:
            self.value += other.value
        else:
            raise BasTypeError(f"cannot add {other.type} to {self.type}")

    # you can only subtract numbers
    def sub(self, other: 'BasLangValue') -> 'BasLangValue':
        if self.type == other.type == "number":
            self.value -= other.value
        else:
            raise BasTypeError(f"cannot subtract {other.type} from {self.type}")
        
    # you can only multiply numbers
    def mul(self, other: 'BasLangValue') -> 'BasLangValue':
        if self.type == other.type == "number":
            self.value *= other.value
        else:
            raise BasTypeError(f"cannot multiply {self.type} by {other.type}")
    
    # you can only divide numbers
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
    

# at some point, I may add other types (like arrays or integers).
# for now, this is enough for a toy language.
