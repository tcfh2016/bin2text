# -*- coding: utf-8 -*-

class LineType(object):
    DefinedStruct      = "D"
    DefinedStructField = "M"

    Struct             = "S"
    StructField        = "F"

    Constant           = "C"

class StructType(object):
    UINT8         = 0
    INT8          = 1
    UINT16        = 2
    INT16         = 3
    UINT32        = 4
    INT32         = 5
    RESERVED      = 6
    FLOAT         = 7
    RESERVED2     = 8
    DOUBLE        = 9

    BOOL          = 10
    ARRAY         = 14

    POINTER       = 15
    NIL_POINTER   = 16

    STRUCT        = 17
    UNION         = 18

    BITSTRUCT     = 19
    FUNCTION      = 20
    PROCEDURE     = 21
    PROCESS       = 22
    SIGNAL        = 23
    TIMER         = 24
    ALARM         = 25

    UINT64        = 26
    INT64         = 27
    UINT128       = 28
    INT128        = 29

    PSEUDOTYPE    = 50

class StructTypeInfo(object):
    NONE     = 0
    ENUM     = 1
    ENUM_VAL = 2
    RANGE    = 3
    NEAR     = 4
    FAR      = 5
    PACKED   = 6
    CONSTANT = 7
