import re

# think I've finally got it working
# here's the breakdown:  |keywords|   numbers   |      strings      | relops |valid symbols| everything else
tokenizer = re.compile(r"([a-z]\w*|\d+(?:\.\d+)?|(?:\"(?:\\.|.)*?\")|>=|<=|!=|[()+\-*\/>=<]|[^\s\w]+)", flags=re.IGNORECASE)

while True:
    line = input(": ")
    if line == "quit":
        break
    print(tokenizer.findall(line))
