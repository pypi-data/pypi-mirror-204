"""Console script for app01."""
import argparse
# import sys
# from argparse import Namespace
import sys

from app01.matt import math_add


# def main():
#     """Console script for app01."""
#     parser = argparse.ArgumentParser()
#     parser.add_argument('_', nargs='*')
#     args = parser.parse_args()
#
#     s = math_add.add_num(args._)
#     print("Arguments: 输出结果: " + str(s))
#
#     # print("Arguments: " + str(args._))
#     # print("Replace this message by putting your code into "
#     #       "app01.cli.main")
#     return 0

def main():
    from app01.config.oss_helper import show_list
    show_list()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
