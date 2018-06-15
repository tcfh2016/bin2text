# -*- coding: utf-8 -*-

class Handler(object):
    def __init__(self, cfg):
        self.cfg = cfg

        self.metadata = None
        self.metadata_handler = None

    def parse(self):
        self._parse_metadata()
        self._preparse()
        self._parse_items()
        self._postparse()

        print "Complete {} converting!".format (self.cfg.bin_file)

    def _parse_metadata(self):
        self.config.init_meta_handler()
        
        self.metadata = self.config.get_metadata()
        self.metadata_handler = self.config.get

        print "parsing meta data..."
        pass

    def _preparse(self):
        print "preparsing..."
        pass

    def _parse_items(self):
        print "parsing items..."
        pass

    def _postparse(self):
        print "doing post parsing..."
        pass

    def _add_metadata_parser(self):
        self.cfg.init_metadata_parser()
