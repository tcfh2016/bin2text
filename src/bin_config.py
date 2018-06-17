# -*- coding: utf-8 -*-
import os

import metadata_handler
import txtcsv_format_handler

class Config(object):
    def __init__(self, opt):
        self.metadata = None
        self.meta_handler = None
        self.outfile_format = "CSV"

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

    def init_meta_handler(self):
        metadata_parse = self.get_metadata()
        metadata_format = txtcsv_format_handler.TxtCsvFormatHandler(self.outfile_format)
        self.meta_handler = [metadata_parse, metadata_format]

    # May call multiply times, use 'metadata' to keep only contruct once.
    def get_metadata(self):
        if self.metadata is None:
            self.metadata = metadata_handler.MetaDataHandler(self.sack_types_file, self.sack_dynamic_file)
        return self.metadata
