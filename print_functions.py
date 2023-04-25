import time
import sys

def print_delay(message, delay):
    print(message)
    time.sleep(delay)

def print_slowly(message, delay):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("")


def print_options(options, delay):
    print_slowly("What do you want to do?", delay)
    for option in options:
        # print(option, ":", options[option])
        print(option, end='')
        print(":", options[option])