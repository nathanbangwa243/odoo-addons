# -*- coding: utf-8 -*-

# add custom addons path to odoo config file

# packages
import os
import sys


def check_args():
    """cmd args assertion
    """
    # check list
    assert len(sys.argv) == 3

    # config file arg
    assert '-cf' in sys.argv

    # check file exist
    assert os.path.isfile(sys.argv[-1])


def main():
    """add custom path to odoo config file
    """

    # line to replace
    old_line = input("[Line to replace]: ")
    new_line = input("[New Line]: ")

    # read data
    with open(sys.argv[-1], 'r') as fp:
        text_data = fp.read()

    # replace old by new
    text_data = text_data.replace(old_line, new_line)

    # write data
    with open(sys.argv[-1], 'w') as fp:
        text_data = fp.write(text_data)

    print(f"[Message] : File '{sys.argv[-1]}' Modified")


if __name__ == "__main__":
    check_args()

    main()
