# types.dat分析

types.dat文件里定义的行类型主要分为C, S, F, D, M五大类。

- C，表示constant，即常量的定义。
- S，表示struct，即结构体定义。
- F，表示field，是结构体内的字段。
- D，表示define，自定义的结构体。
- M，表示自定义结构体的字段。

每行的定义有18项组成，对于不同类型来说每一项可能对应不同的含义。

# 行解析
			 
1. 类型S

-  第0项：行序号。
-  第1项：行类型，固定为S。
-  第2项：数据类型，对应定义的S。
-  第3项：
-  第4项：
-  第5项：字段tag，S可以代表C++里面的struct, union, enum，int, float等所有类型，由此项进行进一步标识。
-  第6项：字段tag描述
-  第7项：
-  第8项：类型大小
-  第9项：0表示内建类型，1表示自定义类型
- 第10项：自定义struct包含的元素个数，对于内建类型为0
- 第11项：自定义struct包含的元素个数（定义为数组的个数需重复计算）
- 第12项：
- 第13项：
- 第14项：
- 第15项：
- 第16项：
- 第17项：

类型S定义结构体，可以对应以下几种数据类型：

- 内建类型，如int, float, double, char等
- union
- enum，enum和UINT32享有相同的字段tag(第5项），因此需要通过tag描述进一步区分（第6项）
- 通过typedef定义的数组
- 定义的struct，第11项的统计会将其中包含的数组字段重复统计


   4710,    S,    EState,    ,    ,    4,    1,    0,    4,    1,    2,    0,    0,    0,    0,    1,    0,    0,    ""
      0,    1,         2,   3,   4,    5,    6,    7,    8,    9,   10,   11,   12,   13,   14,   15,   16,   17,    18
order,  line    typename,    ,field type   tag      ,size ,     ,element    ,     ,     ,     ,     ,     ,     ,     ,
        type,                 type,  tag, info,                   count,
		
2. 类型C

-  第0项：行序号。
-  第1项：行类型，固定为C。
-  第2项：数据类型，对应定义的S。
-  第3项：字段名称
-  第4项：
-  第5项：字段tag
-  第6项：字段tag描述
-  第7项：
-  第8项：
-  第9项：
- 第10项：字段的值
- 第11项：字段的索引
- 第12项：
- 第13项：
- 第14项：
- 第15项：
- 第16项：
- 第17项：

类型C作为S类型的字段使用，由C组成的S类型都被定义为enum。

   90,       C,    EStatusLte,    EStatusLte_Ok,    ,    4,    7,    0,    0,    0,    0,    3,    0,    0,    1,    0,    0,    0,    ""
    0,       1,             2,                3,   4,    5,    6,    7,    8,    9,   10,   11,   12,   13,   14,   15,   16,   17,    18
order,linetype,      type name,      field name,    ,     ,     ,     ,     ,     ,value,index,     ,     ,     ,     ,     ,     ,

		
3. 类型F

-  第0项：行序号。
-  第1项：行类型，固定为C。
-  第2项：数据类型，对应定义的S。
-  第3项：字段名称
-  第4项：字段类型
-  第5项：字段tag，S可以代表C++里面的struct, union, enum，int, float等所有类型，由此项进行进一步标识。
-  第6项：
-  第7项：
-  第8项：字段大小
-  第9项：
- 第10项：字段的值
- 第11项：字段的索引
- 第12项：
- 第13项：
- 第14项：字段的定义层次，也即是SConfigurableUsageAddresses ->SAddressInfo
- 第15项：
- 第16项：
- 第17项：

类型F作为S类型的字段使用。

    30,    F,    SMessageAddress,     board,    TBoard,     0,    0,    0,    1,    0,    0,    0,    0,    0,    1,    1,    0,    26,    ""
     0,    1,                  2,         3,         4,     5,    6,    7,    8,    9,   10,   11,   12,   13,   14,   15,   16,    17,    18
order,  line           type name,field name,field type,      ,     ,     , size,     ,     ,     ,     ,     ,     ,     ,     ,      ,      
        type,

4. 类型D

-  第0项：行序号。
-  第1项：行类型，固定为C。
-  第2项：数据类型，对应定义的S。
-  第3项：字段名称
-  第4项：
-  第5项：字段tag
-  第6项：字段tag描述
-  第7项：
-  第8项：
-  第9项：
- 第10项：字段的值
- 第11项：字段的索引
- 第12项：
- 第13项：
- 第14项：
- 第15项：
- 第16项：
- 第17项：


   927,    D,    43CF,    ,    PS_CA_PUCCH_RESOURCES_REQ_MSG,    23,    0,    0,    52,    0,    12,    13,    0,    0,    0,    1,    0,    0,    ""
    0,     1,       2,   3,                                4,     5,    6,    7,     8,    9,    10,    11,   12,   13,   14,   15,   16,   17,    18
order,  line  message     ,                     message name,      ,     ,     ,  size,     , field extra f
        type,      id,                                                                       number,number,
		
		
5. 类型M

message defined:

message field:		
		#    928,    M,    43CF,    msgHeader,    SMessageHeader,    17,    0,    0,    16,    0,    5,    0,    0,    0,    1,    1,    0,    37,    ""
    #      0,    1,       2,            3,                 4,     5,    6,    7,     8,    9,   10,   11,   12,   13,   14,   15,   16,    17,    18
    # order,  line  message    field name,        field type,      ,     , byte   size,     ,     ,     ,     ,     ,     ,     ,     ,      ,
    #         type,      id,                                             offset,


		
		