# -*- coding: utf-8 -*-

import  argparse

import  config
import  handler

# command line pattern:
# python bin2text.py --config-dir profile_directory --bin bin_file --type csv
def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("--config-dir", required=True,
                        help="specify the profile directory.")
    parser.add_argument("--bin", required=True,
                        help="bin file which needed to be parsed.")
    parser.add_argument("--type", default='csv',
                        help="target file format.")

    return parser.parse_args()

def main():
    opt = parse_args()

    cfg = config.Config(opt)
    parser = handler.Handler(cfg)
    parser.parse()

if __name__ == "__main__":
    main()
