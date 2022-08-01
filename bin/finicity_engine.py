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
    parser.add_argument(
            "--token",
            "-t",
            required=False,
            default=None,
            help="finicity access token"
            )
    parser.add_argument(
            "--body",
            "-b",
            required=False,
            default=None,
            help="finicity body to post api"
            )
    parser.add_argument(
            "--params",
            "-p",
            required=False,
            default=None,
            help="finicity params to get api"
            )
    parser.add_argument(
            "--customer_id",
            "-id",
            required=False,
            default=None,
            help="finicity customer_id"
            )

    return parser.parse_args()


def get_value(action):
    if action == "create_token":
        return create_token(action)
    elif action == "add_customer":
        return add_customer(action, f_token, f_body) 
    elif action == "get_customers":
        return get_customers(action, f_token, f_params)
    elif action == "get_customer_by_id":
        return get_customer_by_id(action, f_token, f_customer_id)
    elif action == "delete_customer_by_id":
        return delete_customer_by_id(action, f_token, f_customer_id)


def main(args):
    if len(args) < 2:
        usage()

    global f_token, f_body, f_params, f_customer_id 

    args = get_args()
    f_action = args.action
    f_token = args.token
    f_body = eval(args.body) if args.body else {}
    f_params = eval(args.params) if args.params else {}
    f_customer_id = args.customer_id
    return_value = get_value(f_action)
    print(return_value)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as ex:
        raise ex

