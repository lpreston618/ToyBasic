from toyBasic import *

a = BasLangValue(init_value=2)
b = BasLangValue(init_value=3)
s = BasLangValue(init_type="string", init_value="Hello, World!")
z = BasLangValue(init_type="string", init_value="AbCdEfG098712")

try:
    print(a.add(b).value)
    print(b.compare(a))

    print(z.value)
    z.compare(a)
except BasLangError as err:
    print("Error: " + err.message)
