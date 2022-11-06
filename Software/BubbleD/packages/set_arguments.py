"""
Author: Divya Pal
Institute: Physikalisches Institut, Universität Bonn
Modified: Mar 2022
"""

import argparse
import os


def dir_path(path):
    '''Verifies if provided directory path is valid'''
    if not os.path.isdir(path):
        raise ValueError(f"{path} is not a valid directory")
    return path


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--controller", choices=('True', 'False'),
                    default='True',
                    help="Start GUI with/without external controller"
                    )
# Note1: If -c is False, port value is unused
parser.add_argument("-p", "--port",
                    help="Port connected to the external controller"
                    )
# Note2: If port value is not provided it is imported from config.ini file
parser.add_argument("-t", "--table", choices=('1', '2'),
                    default='1',
                    help="Choose table to load config file"
                    )

parser.add_argument("-cfg", "--config",
                    default='.',
                    help="Insert directory to read/write config_table1.ini or "
                    "config_table2.ini"
                    )

# importing the provided arguments
args = parser.parse_args()
