# -*- coding: utf-8 -*-

class Metadata(object):
    pass

class MetadataArray(Metadata):
    pass

class MetadataStruct(Metadata):
    pass

class MetadataUnion(Metadata):
    pass

class MetadataEnum(Metadata):
    def __init__(self, name, size, size_in_bits, constant_num):
        self.name = name
        self.size = size

        self.size_in_bits = size_in_bits
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
