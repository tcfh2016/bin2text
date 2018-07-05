# -*- coding: utf-8 -*-

import datatype
import logging

class Metadata(object):
    pass

class MetadataBasicType(object):
    basic_type_info = {
        datatype.StructType.UINT8:       ("_anon_uint8", 1, "B"),
        datatype.StructType.UINT16:      ("_anon_uint16", 2, "H"),
        datatype.StructType.UINT32:      ("_anon_uint32", 4, "I"),
        datatype.StructType.UINT64:      ("_anon_uint64", 8, "Q"),
        datatype.StructType.UINT128:     ("_anon_uint128", 16, "QQ"),

        datatype.StructType.INT8:        ("_anon_int8", 1, "b"),
        datatype.StructType.INT16:       ("_anon_int16", 2, "h"),
        datatype.StructType.INT32:       ("_anon_int32", 4, "i"),
        datatype.StructType.INT64:       ("_anon_int64", 8, "q"),
        datatype.StructType.INT128:      ("_anon_int128", 16, "qq"),

        datatype.StructType.BOOL:        ("_anon_bool", 1, "?"),
        datatype.StructType.FLOAT:        ("_anon_real", 4, "f"),
        datatype.StructType.DOUBLE:  ("_anon_doublereal", 8, "d"),
    }

    def __init__(self, field_struct_type):
        (self._name, self._size, self._alia) = self.basic_type_info[field_struct_type]

    def __eq__(self, another):
        return ((self._name == another._name) and
                (self._size == another._size) and
                (self._alia == another._alia))

class MetadataArray(Metadata):
    def __init__(self, name, size, element_number, element_metadata=None):
        self._name = name
        self._size = size
        self._element_number = element_number
        self._element_metadata = element_metadata

class MetadataStruct(Metadata):
    def __init__(self, name, size, field_number, array_field_number):
        self.logger = logging.getLogger(__name__)
        self._name = name
        self._size = size
        self._field_number = field_number
        self._array_field_number = array_field_number
        self._has_array_field = False
        self._parsed_field_counter = 0
        self._fields = []

        if array_field_number > 0:
            self._has_array_field = True
    def __str__(self):
        return ("MetadataStruct(_name:%s, _size:%d, _field_number:%d, _array_field_number:%d, _fields:%s)" %
                          (self._name, self._size, self._field_number, self._array_field_number, self._fields))
    def __eq__(self, another):
        return ( (self._name == another._name) and
                 (self._size == another._size) and
                 (self._field_number == another._field_number) and
                 (self._array_field_number == another._array_field_number) and
                 (self._fields == another._fields) )

    def add_field(self, name, type_name, field_struct_type, meta, offset, size):
        new_field = Field(self._field_number, name, type_name, field_struct_type,
                          meta, offset, size)
        self._fields.append(new_field)
        self._parsed_field_counter += 1
        self.logger.info("MetadataStruct.add_field:[%s,%s,%s,%s,%d,%d] parsed_field_number=%d" %
                         (name, type_name, field_struct_type, meta, offset, size, self._parsed_field_counter))


class MetadataUnion(Metadata):
    def __init__(self, name, size, field_number):
        self._name = name
        self._size = size
        self._field_number = field_number

class MetadataEnum(Metadata):
    def __init__(self, name, size, constant_num):
        self.name = name
        self.size = size

        self.constant_num = constant_num
        self.constants = []

    def add_field(self, value):
        self.constants.append(value)
        self.constant_num += 1

class MetadataMessage(Metadata):
    __HeaderTypeName = "SMessageHeader"
    __HeaderSize = 16

    @staticmethod
    def is_header(field_name, field_size, field_offset):
        return (field_name == MetadataMessage.__HeaderTypeName
                and field_size == MetadataMessage.__HeaderSize
                and field_offset == 0)

    def __init__(self, id, name, size, field_num, variable_array_field_num):
        self.name = name
        self.size = size
        self.has_header = False

        self.id = id
        self.field_num = field_num
        self.variable_array_field_num = variable_array_field_num

class Field(object):
    def __init__(self, index, name, type_name, field_struct_type, meta, offset, size):
        self._index = index
        self._name = name
        self._typename = type_name
        self._field_struct_type = field_struct_type
        self._metadata = meta
        self._offset = offset
        self._size = size
