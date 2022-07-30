import argparse
import sys

from finicity_utils import *

def usage():
    print("""
            usgae:
            python3 finicity_engine.py create_token
          """
          )
    sys.exit(-1)



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "action", 
            help="actions to be performed on finicity_api"
            )
    return parser.parse_args()


def get_value(action):
    if action == "create_token":
        return create_token(action)


def main(args):
    if len(args) < 2:
        usage()

    args = get_args()
    fin_action = args.action
    return_value = get_value(fin_action)
    print(return_value)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as ex:
        raise ex

