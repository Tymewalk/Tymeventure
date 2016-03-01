import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name",
                    help="Set your name")
parser.add_argument("--nocolor", help="Turn off colors",
                    action="store_true")
parser.add_argument("--nointro", help="Skip the intro, best used with -n",
                    action="store_true")
args = parser.parse_args()
