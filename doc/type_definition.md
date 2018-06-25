# types.dat分析

types.dat文件里定义的行类型主要分为C, S, F, D, M五大类。

- C，表示constant，即常量的定义。
- S，表示struct，即结构体定义。
- F，表示field，是结构体内的字段。
- D，表示define，自定义的结构体。
- M，表示自定义结构体的字段。

每行的定义有18项组成，对于不同类型来说每一项可能对应不同的含义。

# 行解析

1. 常量定义（C）

- 第0项：行序号。
- 第1项：行类型，固定为C。
- 第2项：数据类型，对应定义的S。
- 第3项：字段名称
- 第4项：-->>无意义
- 第5项：字段tag
- 第6项：字段tag描述
- 第7项：字段偏移
- 第8项：字段大小
- 第9项：
- 第10项：
- 第0项：
- 第0项：
- 第0项：
- 第0项：
- 第0项：
- 第0项：
- 第0项：

   90,       C,    EStatusLte,    EStatusLte_Ok,    ,    4,    7,    0,    0,    0,    0,    3,    0,    0,    1,    0,    0,    0,    ""
    0,       1,             2,                3,   4,    5,    6,    7,    8,    9,   10,   11,   12,   13,   14,   15,   16,   17,    18
order,linetype,      type name,       field name,    ,     ,     ,     ,     ,     ,value,index,     ,     ,     ,


			 
2. S与F类型

3. D与M类型



message defined:

    #    927,    D,    43CF,    ,    PS_CA_PUCCH_RESOURCES_REQ_MSG,    23,    0,    0,    52,    0,    12,    13,    0,    0,    0,    1,    0,    0,    ""
    #     0,     1,       2,   3,                                4,     5,    6,    7,     8,    9,    10,    11,   12,   13,   14,   15,   16,   17,    18
    # order,  line  message     ,                     message name,      ,     ,     ,  size,     , field extra f
    #         type,      id,                                                                       number,number,
		
message field:		
		#    928,    M,    43CF,    msgHeader,    SMessageHeader,    17,    0,    0,    16,    0,    5,    0,    0,    0,    1,    1,    0,    37,    ""
    #      0,    1,       2,            3,                 4,     5,    6,    7,     8,    9,   10,   11,   12,   13,   14,   15,   16,    17,    18
    # order,  line  message    field name,        field type,      ,     , byte   size,     ,     ,     ,     ,     ,     ,     ,     ,      ,
    #         type,      id,                                             offset,

struct defined:		
		#    4710,    S,    EState,    ,    ,    4,    1,    0,    4,    1,    2,    0,    0,    0,    0,    1,    0,    0,    ""
    #       0,    1,         2,   3,   4,    5,    6,    7,    8,    9,   10,   11,   12,   13,   14,   15,   16,   17,    18
    # order,  line    typename,    ,field type   tag      ,size ,     ,element    ,     ,     ,     ,     ,     ,     ,     ,
    #         type,                 type,  tag, info,                   count,
		
constant defined:		
		
		