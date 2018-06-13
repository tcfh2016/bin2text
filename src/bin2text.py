# -*- coding: utf-8 -*-

import  argparse

parser = argparse.ArgumentParser()

parser.add_argument("--config-dir", required=True,
                    help="specify the profile directory.")
parser.add_argument("--bin", required=True,
                    help="bin file which needed to be parsed.")
parser.add_argument("--type", default='csv',
                    help="target file format.")

args = parser.parse_args()

# python bin2text.py --config-dir profile_directory --bin bin_file --type csv
