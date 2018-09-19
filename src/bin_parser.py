# -*- coding: utf-8 -*-

import pdb
class Parser(object):
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
        print "parsing meta data..."
        #pdb.set_trace()
        self.metadata = self.cfg.get_metadata()
        self.__add_metadata_handler()

        self.__init_handler(self.metadata_handler)
        self.__handle(self.metadata_handler, self.metadata)
        self.__destroy_handler(self.metadata_handler)

    def _preparse(self):
        print "preparsing..."
        pass

    def _parse_items(self):
        print "parsing items..."
        pass

    def _postparse(self):
        print "doing post parsing..."
        pass

    def __add_metadata_handler(self):
        self.cfg.init_meta_handler()
        self.metadata_handler = self.cfg.meta_handler

    def __add_message_handler(self):
        pass

    def __init_handler(self, handler_list):
        for h in handler_list:
            h.init()
    def __handle(self, handler_list, message):
        for h in handler_list:
            h.process(message)

    def __destroy_handler(self, handler_list):
        for h in handler_list:
            h.destroy()
