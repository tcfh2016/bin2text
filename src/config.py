# -*- coding: utf-8 -*-
import os

class Config(object):
    def __init__(self, opt):
        self.config_dir = opt.config_dir
        if (not os.path.isdir(self.config_dir)):
            print "config_dir is not a directory."
            os._exit(0)

        self.bin_file = opt.bin
        if (not self.check_file_availability(self.bin_file)):
            print "bin_file is not available."
            os._exit(0)

        self.sack_types_file = os.path.join(self.config_dir, "types.dat")
        if (not self.check_file_availability(self.sack_types_file)):
            print "types.dat is not available."
            os._exit(0)

        self.sack_dynamic_file = os.path.join(self.config_dir, "csack_config.xml")
        if (not self.check_file_availability(self.sack_dynamic_file)):
            print "csack_config.xml is not available."
            os._exit(0)

    def check_file_availability(self, f):
        if (os.path.isfile(f) and os.access(f, os.R_OK)):
            return True
        else:
            return False
