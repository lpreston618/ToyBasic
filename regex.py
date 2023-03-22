import re

tokenizer = re.compile(r"([a-z]\w*|\d+(?:\.\d+)?|>=|<=|!=|[()+\-*\/>=<]|[^\s\w]+)", flags=re.IGNORECASE)

while True:
    line = input(": ")
    if line == "quit":
        break
    print(bigone.findall(line))
