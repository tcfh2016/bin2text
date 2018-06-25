# -*- coding: utf-8 -*-

class LineType(object):
    DefinedStruct      = "D"
    DefinedStructField = "M"

    Struct             = "S"
    StructField        = "F"

    Constant           = "C"


class Tag(object):
    NONE     = 0
    ENUM     = 1
    ENUM_VAL = 2
    RANGE    = 3
    NEAR     = 4
    FAR      = 5
    PACKED   = 6
    CONSTANT = 7
