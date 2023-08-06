#!/bin/sh

import argparse

from generator import password_generator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--length", "-L", type=int, required=True, help="length of a password")
    parser.add_argument("-n", "--number", "-N", type=int, required=True, help="number of generated password")
    parser.add_argument("-c", "--check", "-C", action="store_true", help="check the passwords")
    parser.add_argument("-e", "--eval", "-E", action="store_true", help="eval the passwords")
    parser.add_argument("--digit", "--Digit", "--DIGIT", action="store_true", help="use digits in the generation")
    parser.add_argument("--lowercase", "--LOWERCASE", "-Lowercase", action="store_true",
                        help="use lowercase in the generation")
    parser.add_argument("--uppercase", "--UPPERCASE", "--Uppercase", action="store_true",
                        help="use uppercase in the generation")
    parser.add_argument("--symbol", "--SYMBOL", "--SYMBOL", action="store_true", help="use symbols in the generation")
    args = parser.parse_args()

    digit = False
    lowercase = False
    uppercase = False
    symbol = False
    check = False
    eval = False

    if args.digit:
        digit = True
    if args.lowercase:
        lowercase = True
    if args.uppercase:
        uppercase = True
    if args.symbol:
        symbol = True
    if args.check:
        print("PLEASE NOTE THAT")
        check = True

    if args.eval:
        eval = True

    password_generator(args.length, args.number, tocheck=check, toeval=eval, digit=digit, lowercase=lowercase, uppercase=uppercase, symbol=symbol)


if __name__ == "__main__":
    main()
