import string, random

alp = string.digits + string.ascii_lowercase + string.ascii_uppercase

def generate():
    return ''.join([random.choice(alp) for i in range(32)])

ARRAY = [generate() for i in range(2048])

with open("array.txt", "w") as f:
    print(" ".join(ARRAY), file=f)

