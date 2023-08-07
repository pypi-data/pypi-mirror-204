"""The main entry point. Invoke as for app02."""

import argparse
import sys


def main():
    """Console script for app02."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    from app02.matt.math_add import add_num

    print(add_num([1, 2, 3, 4, 55, 6, 6, 7, 30, 9, 9, 0, ]))

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "app02.cli.main")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
