import string
import random as rd
from checker import check
from eval import password_strength


def password_generator(length: int, number: int,
                       tocheck: bool = False, toeval: bool = False,
                       digit: bool = False, lowercase: bool = False,
                       uppercase: bool = False, symbol: bool = False):
    """
    :param length: The length of the generated password
    :param number: The number of generated password needed
    :param tocheck: If you want to check if the generated password has been exposed via the xposedornot API
    :param toeval: If you want to simply eval the quality of your password on a scale of ten
    :param digit: If you want that your password contain digits/numbers (it can be combined with the following args)
    :param lowercase: If you want that your password contain lowercase letters
    :param uppercase: If you want that your password contain uppercase letters
    :param symbol: If you want that your password contain symbol/punctuation
    """
    char = []

    if not (digit or lowercase or uppercase or symbol):
        char = list(string.printable)[:-6]

    if digit:
        char += string.digits

    if lowercase:
        char += string.ascii_lowercase

    if uppercase:
        char += string.ascii_uppercase

    if symbol:
        char += string.punctuation

    for i in range(number):
        global password
        password = []
        password = [""] * length

        for j in range(length):
            password.append(char[rd.randint(0, len(char) - 1)])

        if tocheck and toeval:
            if check(''.join(password)):
                print(f"{i + 1}. {''.join(password)} {password_strength(str(password))}/10")

        elif tocheck:
            if check(''.join(password)):
                print(f"{i + 1}. {''.join(password)} {password_strength(str(password))}/10")

        elif toeval:
            print(f"{i + 1}. {''.join(password)} {password_strength(str(password))}/10")

        else:
            print(f"{i + 1}. {''.join(password)}")

    print(f"{i + 1} passwords were generated")
