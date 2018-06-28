# -*- coding: utf-8 -*-
import re

import handler
import datatype
import metadata

class MetaDataHandler(handler.Handler):
    def __init__(self, types_file, dynamic_file):
        self._type_filename = types_file
        self._dynamic_filename = dynamic_file
        self._metadata_message = {}
        self._metadata = {}

        self._lines = None
        self._linenumber = 0

        self._specified_item_num = 19

    def process(self, msg):
        if self._lines is None:
            with open(self._type_filename, "rb") as f:
                self._lines = f.read().split("\n")

        # skip blank line.
        blankline_regex = re.compile("^\s*$")

        for line in self._lines:
            if blankline_regex.match(line):
                continue

            self._linenumber += 1
            items = line.split(",", self._specified_item_num - 1)
            if not self._valid_items(items):
                print "invalid fromat in %s, content:%s" %(self._type_filename, items)
                continue

            self._parse_item(items)

        print "start to do metadata handling."
        print "\t %d lines in %s." % (self._linenumber, self._type_filename)

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
            self._parse_constant(items)
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
        assert msg_id not in self._metadata_message
        self._metadata_message[msg_id] = meta_message

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

        assert msg_id in self._metadata_message
        metamessage = self._metadata_message[msg_id]

        if metadata.MetadataMessage.is_header(field_name, field_size, field_offset):
            metamessage.has_header = True
            return

        self._parse_field(items, meta_message)


    #    90,    C,    EStatusLte,    EStatusLte_Ok,    ,    4,    7,    0,    0,    0,    0,    3,    0,    0,    1,    0,    0,    0,    ""
    #     0,    1,             2,                3,   4,    5,    6,    7,    8,    9,   10,   11,   12,   13,   14,   15,   16,   17,    18
    # order, line      type name,       field name,    ,     ,     ,     ,     ,     ,value,index,     ,     ,     ,     ,     ,     ,
    #        type,
    def _parse_constant(self, items):
        belongs_enum_type = items[2]   # 所属的enum名称，如 EInetRouteOperation

        field_name = items[3]
        field_value = items[10]
        field_index = items[11]

        meta_enum = None
        if belongs_enum_type not in self.metadata:
            print "The Enum type was not ready, something maybe wrong."
            meta_enum = metadata.MetadataEnum(belongs_enum_type, 4, 0)
            self._metadata[belongs_enum_type] = meta_enum
        else:
            meta_enum = self._metadata[belongs_enum_type]

        meta_enum.add_field((field_index, field_value, field_name))


    #    4710,    S,    EState,    ,    ,    4,    1,    0,    4,    1,    2,    0,    0,    0,    0,    1,    0,    0,    ""
    #       0,    1,         2,   3,   4,    5,    6,    7,    8,    9,   10,   11,   12,   13,   14,   15,   16,   17,    18
    # order,  line    typename,    ,field type   tag      ,size ,     ,element    ,     ,     ,     ,     ,     ,     ,     ,
    #         type,                 type,  tag, info,                   count,

    def _parse_struct(self, items):
        type_name = items[2]            # 类型名称，如 EState, int, float
        struct_type = items[5]          # 自定义类型，进一步区分enum, union, int, float
        struct_type_info = items[6]     # Enum 为 1.
        struct_size = items[8]          # 类型大小（字节）
        struct_field_number = items[10] # 包含的成员个数，自定义类型成员个数 > 0

        if struct_type == datatype.StructType.ARRAY:
            meta_array = metadata.MetadataArray(type_name, struct_size, struct_field_number)
            self._metadata[type_name] = meta_array
        elif struct_type == datatype.StructType.STRUCT:
            field_number_plus_array_elementnumber = items[11]
            array_field_num = field_number_plus_array_elementnumber - struct_field_number
            meta_struct = metadata.MetadataStruct(type_name,
                                                  struct_size,
                                                  struct_field_number,
                                                  array_field_num)
            self._metadata[type_name] = meta_struct
        elif struct_type == datatype.StructType.UNION:
            meta_union = metadata.MetadataArray(type_name, struct_size, struct_field_number)
            self._metadata[type_name] = meta_union
        else:
            type_info = items[6]
            if type_info == datatype.StructTypeInfo.ENUM:
                meta_enum = metadata.MetadataEnum(type_name, struct_size, struct_field_number)
                self._metadata[type_name] = meta_enum
            else:
                print "UNKNOW DATA TYPE."


    #    928,    M,    43CF,    msgHeader,    SMessageHeader,    17,    0,    0,    16,    0,    5,    0,    0,    0,    1,    1,    0,    37,    ""
    #      0,    1,       2,            3,                 4,     5,    6,    7,     8,    9,   10,   11,   12,   13,   14,   15,   16,    17,    18
    # order,  line  message    field name,        field type,      ,     , byte   size,     ,     ,     ,     ,     ,     ,     ,     ,      ,
    #         type,      id,                                             offset,

    def _parse_struct_field(self, items):
        belongs_struct_name = items[2]   # 所属的struct名称，如 SMessageAddress
        assert belongs_struct_name in self._metadata

        meta_struct = self._metadata[belongs_struct_name]
        self._parse_field(items, meta_struct)


    def _valid_items(self, items):
        if len(items) != self._specified_item_num:
            print "items number excess %d" % self._specified_item_num
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


    def _parse_field(self, items, meta_struct):
        # items 对应“F”行。
        # meta_struct 对应从“S”行解析出来的 MetadataStruct/MetadataUnion/MetadataArray/MetadataEnum
        # 算法目的：将所有自定义的类型收集起来。
        # 算法逻辑：
        # 1. 递归找到最底层的“S”类型
        # 2. 将其存储到 self._metadata 字典中
        # 举例：

        raw_field_meta, fields_name = self._get_field_meta(items, meta_struct, 1)

        # 解析当前字段对应的meta
        blongs_struct_name = items[2]
        field_name = items[3]
        field_type_name = items[4]
        field_struct_type = items[5]

        field_meta = self._parse_field_meta(items, raw_field_meta, field_type_name, field_struct_type)

        if isinstance(raw_field_meta, (metadata.MetadataStruct)):
            field_byte_offset = items[7]
            field_size = items[8]
            raw_field_meta.add_field(field_name, field_type_name, field_struct_type, field_meta, field_byte_offset, field_size)
        else:
            pass

    # recursive function to get field meta data.
    def _get_field_meta(self, items, meta_data, parse_level):
        field_level = items[14] # 该"F"在"S"中的层次。
        assert field_level < 32

        if field_level == parse_level:
            return meta_data, ""
        '''
        if isinstance(meta_data, metadata.MetadataArray):
            return meta_data, ""
        elif isinstance(meta_data, (metadata.MetadataStruct,
                                    metadata.MetadataUnion,
                                    metadata.MetadataMessage)):
            return meta_data, ""
        else:
            return meta_data, ""
        '''

    def _parse_field_meta(self, items, meta_data, field_type_name, field_struct_type):
        meta_result = None
        struct_size = items[8]          # 类型大小（字节）
        struct_field_number = items[10] # 包含的成员个数，自定义类型成员个数 > 0

        if field_type_name != "":
            return None
        elif field_struct_type == datatype.StructType.STRUCT:
            field_number = items[10]
            field_number_plus_array_elementnumber = items[11]
            array_field_num = field_number_plus_array_elementnumber - struct_field_number
            meta_result = metadata.MetadataStruct(type_name,
                                                  struct_size,
                                                  struct_field_number,
                                                  array_field_num)

        elif field_struct_type == datatype.StructType.ARRAY:
            meta_result = metadata.MetadataArray(field_type_name, struct_size, struct_field_number)
        elif struct_type == datatype.StructType.UNION:
            meta_result = metadata.MetadataArray(field_type_name, struct_size, struct_field_number)
        else:
            type_info = items[6]
            if type_info == datatype.StructTypeInfo.RANGE:
                pass
            else:
                meta_struct = metadata.MetadataBasicType(field_struct_type)

        return meta_struct
