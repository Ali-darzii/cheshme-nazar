from random import randint


def generate_otp() -> int:
    return randint(10000, 99999)