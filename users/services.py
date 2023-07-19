import random


def generate_code():
    random.seed()
    return str(random.randint(10000, 99999))

