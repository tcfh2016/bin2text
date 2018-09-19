# -*- coding: utf-8 -*-

import  argparse
import  logging

import  bin_config
import  bin_parser

# command line pattern:
# python bin2text.py --config-dir profile_directory --bin bin_file --type csv
def parse_args():

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("--config-dir", required=True,
                        help="specify the profile directory.")
    arg_parser.add_argument("--bin", required=True,
                        help="bin file which needed to be parsed.")
    arg_parser.add_argument("--type", default='csv',
                        help="target file format.")

    return arg_parser.parse_args()

def main():    
    opt = parse_args()

    cfg = bin_config.Config(opt)
    par = bin_parser.Parser(cfg)
    par.parse()

if __name__ == "__main__":
    main()
