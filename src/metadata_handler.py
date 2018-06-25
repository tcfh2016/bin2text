# -*- coding: utf-8 -*-
import re

import handler
import datatype
import metadata

class MetaDataHandler(handler.Handler):
    def __init__(self, types_file, dynamic_file):
        self.type_filename = types_file
        self.dynamic_filename = dynamic_file
        self.metadata_message = {}
        self.metadata = {}

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
            self._parse_message(items)
        elif line_type == datatype.LineType.DefinedStructField:
            self._parse_message_field(items)
        elif line_type == datatype.LineType.Struct:
            self._parse_struct(items)
        elif line_type == datatype.LineType.StructField:
            self._parse_struct_field(items)
        elif line_type == datatype.LineType.Constant:
            self._parse_enum(items)
        else:
            pass

    #    927,    D,    43CF,    ,    PS_CA_PUCCH_RESOURCES_REQ_MSG,    23,    0,    0,    52,    0,    12,    13,    0,    0,    0,    1,    0,    0,    ""
    #     0,     1,       2,   3,                                4,     5,    6,    7,     8,    9,    10,    11,   12,   13,   14,   15,   16,   17,    18
    # order,  line  message     ,                     message name,      ,     ,     ,  size,     , field extra f
    #         type,      id,                                                                       number,number,
    def _parse_message(self, items):
        msg_id = items[2]
        msg_name = items[4]
        msg_size = items[8]
        msg_field_number = items[10]
        msg_extrafield_number = items[11]

        try:
            message_id = int(msg_id, 16)
        except:
            print "_parse_message: invalid msg_id %s" %msg_id
        meta_message = metadata.MetadataMessage(msg_id, msg_name, msg_size,
                                                msg_field_number,
                                                msg_extrafield_number - msg_field_number)
        assert msg_id not in self.metadata_message
        self.metadata_message[msg_id] = meta_message

    #    928,    M,    43CF,    msgHeader,    SMessageHeader,    17,    0,    0,    16,    0,    5,    0,    0,    0,    1,    1,    0,    37,    ""
    #      0,    1,       2,            3,                 4,     5,    6,    7,     8,    9,   10,   11,   12,   13,   14,   15,   16,    17,    18
    # order,  line  message    field name,        field type,      ,     , byte   size,     ,     ,     ,     ,     ,     ,     ,     ,      ,
    #         type,      id,                                             offset,

    def _parse_message_field(self, items):
        msg_id = items[2]
        field_name = items[3]
        field_type = items[4]
        field_offset = items[7]
        field_size = items[8]

        try:
            message_id = int(msg_id, 16)
        except:
            print "_parse_message_field: invalid msg_id %s" %msg_id

        assert msg_id in self.metadata_message
        meta_message = self.metadata_message[msg_id]

        if metadata.MetadataMessage.is_header(field_name, field_size, field_offset):
            meta_message.has_header = True
            return

        self._parse_field(items, meta_message)

    #    4710,    S,    EState,    ,    ,    4,    1,    0,    4,    1,    2,    0,    0,    0,    0,    1,    0,    0,    ""
    #       0,    1,         2,   3,   4,    5,    6,    7,    8,    9,   10,   11,   12,   13,   14,   15,   16,   17,    18
    # order,  line    typename,    ,field type   tag      ,size ,     ,element    ,     ,     ,     ,     ,     ,     ,     ,
    #         type,                 type,  tag, info,                   count,

    def _parse_struct(self, items):
        pass


    #    928,    M,    43CF,    msgHeader,    SMessageHeader,    17,    0,    0,    16,    0,    5,    0,    0,    0,    1,    1,    0,    37,    ""
    #      0,    1,       2,            3,                 4,     5,    6,    7,     8,    9,   10,   11,   12,   13,   14,   15,   16,    17,    18
    # order,  line  message    field name,        field type,      ,     , byte   size,     ,     ,     ,     ,     ,     ,     ,     ,      ,
    #         type,      id,                                             offset,

    def _parse_struct_field(self, items):
        pass


    #    90,    C,    EStatusLte,    EStatusLte_Ok,    ,    4,    7,    0,    0,    0,    0,    3,    0,    0,    1,    0,    0,    0,    ""
    #     0,    1,             2,                3,   4,    5,    6,    7,    8,    9,   10,   11,   12,   13,   14,   15,   16,   17,    18
    # order, line      type name,       field name,    ,     ,     ,     ,     ,     ,value,index,     ,     ,     ,
    #        type,
    def _parse_enum(self, items):
        type_name = items[2]

        field_name = items[3]
        field_value = items[10]
        field_index = items[11]

        meta_enum = None
        if type_name not in self.metadata:
            meta_enum = metadata.MetadataEnum(type_name, 4, 4*8, 0)
            self.metadata[type_name] = meta_enum
        else:
            meta_enum = self.metadata[type_name]

        meta_enum.add_field((field_index, field_value, field_name))

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


    def _parse_field(self, items, meta_data):
        # STEP 1:
        field_meta, fields_name = self._get_field_meta(items, meta_data, 1)

        # STEP 2:
        type_name = items[2]
        field_name = items[3]
        field_type_name = items[4]

        # STEP 3:

    # recursive function to get field meta data.
    def _get_field_meta(self, items, meta_data, parse_level):
        field_level = items[14]
        assert field_level < 32

        if field_level == parse_level:
            return meta_data, ""

        if isinstance(meta_data, metadata.MetadataArray):
            return meta_data, ""
        elif isinstance(meta_data, (metadata.MetadataStruct,
                                    metadata.MetadataUnion,
                                    metadata.MetadataMessage)):
            return meta_data, ""
        else:
            return meta_data, ""
