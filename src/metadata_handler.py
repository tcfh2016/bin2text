# -*- coding: utf-8 -*-
import re

import handler
import datatype

class MetaDataHandler(handler.Handler):
    def __init__(self, types_file, dynamic_file):
        self.type_filename = types_file
        self.dynamic_filename = dynamic_file

        self.lines = None
        self.linenumber = 0

        self.specified_item_num = 19

    def process(self, msg):
        if self.lines is None:
            with open(self.type_filename, "rb") as f:
                self.lines = f.read().split("\n")

        # skip blank line.
        blankline_regex = re.compile("^\s*$")

        for line in self.lines:
            if blankline_regex.match(line):
                continue

            items = line.split(",", self.specified_item_num - 1)
            if not self._valid_items(items):
                print "invalid fromat in %s, content:%s" %(self.type_filename, items)
                continue

            self._parse_item(items)

        print "start to do metadata handling."
        print "\t %d lines in %s." % (self.linenumber, self.type_filename)

    def _parse_item(self, items):
        line_type = items[1]

        if line_type == datatype.LineType.DefinedStruct:
            #self._parse_message(item_list)
            pass

        elif line_type == datatype.LineType.Struct:
            #self._parse_struct(item_list)
            pass

        elif line_type == datatype.LineType.DefinedStructField:
            #self._parse_message_field(item_list)
            pass

        elif line_type == datatype.LineType.StructField:
            #self._parse_struct_field(item_list)
            pass

        elif line_type in (datatype.LineType.EnumValue, datatype.LineType.Constant, datatype.LineType.Constant):
            #self._parse_enum(item_list)
            pass
        else:
            pass
    
    def _valid_items(self, items):
        if len(items) != self.specified_item_num:
            print "items number excess %d" % self.specified_item_num
            return False
        try:
            items[5] = int(items[5])
            items[6] = int(items[6])
            items[7] = int(items[7])
            items[8] = int(items[8])
            items[9] = int(items[9])
            items[10] = int(items[10])
            items[11] = int(items[11])
            items[14] = int(items[14])
            return True
        except:
            return False
