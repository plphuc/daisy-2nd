import os


def handle(*args):
    # run clean_up.sh script, the script is in the same directory as this file
    print("Running post deployment hook")

    os.system(f"sh {os.path.dirname(os.path.realpath(__file__))}/clean_up.sh")
