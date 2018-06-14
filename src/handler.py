# -*- coding: utf-8 -*-

class Handler(object):
    def __init__(self, cfg):
        self.cfg = cfg

    def parse(self):
        self._parse_metadata()
        self._preparse()
        self._parse_items()
        self._postparse()

        print "Complete {} converting!".format (self.cfg.bin_file)

    def _parse_metadata(self):
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
