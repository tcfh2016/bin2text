# -*- coding: utf-8 -*-

class Metadata(object):
    pass

class MetadataArray(Metadata):
    def __init__(self, name, size, field_number):
        self._name = name
        self._size = size
        self._field_number = field_number

class MetadataStruct(Metadata):
    def __init__(self, name, size, field_number, array_field_number):
        self._name = name
        self._size = size
        self._field_number = field_number
        self._array_field_number = array_field_number
        self._has_array_field = False
        self._fields = []

        if array_field_number > 0:
            self._has_array_field = True

    def add_field(self, name, type_name, field_struct_type, meta, offset, size):
        new_field = Field(self._field_number, name, type_name, field_struct_type,
                          meta, offset, size)
        self._fields.append(new_field)
        self._field_number += 1


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
