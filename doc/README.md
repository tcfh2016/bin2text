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

类型解析算法：

首先： 递归找到最底层的“S”类型。
其次： 将其存储到字典中。

注：
① 如果field的自定义类型不为空，相当于表明这些字段已经在之前定义过，那么此时metadata就为空。
② 如果field的自定义类型为空，共有12种类型，还需要进一步解析（类似于解析“S”类型）：
	0,1 --> INT8	
	2   --> UINT16
	3   --> INT16
	4   --> UINT32	
	5   --> INT32
	14  --> ARRAY   -->
	15  --> POINTER -->
	17  --> STRUCT  --> 再创建object
	18  --> UNION	-->
	26  --> UINT64
	27  --> INT64
         
		 
解析举例1：自定义的类型的字段。

```
29,S,SMessageAddress,,,17,0,0,4,0,3,3,0,0,0,1,0,0,""
30,F,SMessageAddress,board,TBoard,0,0,0,1,0,0,0,0,0,1,1,0,26,""
31,F,SMessageAddress,cpu,TCpu,0,0,1,1,0,0,0,0,0,1,1,0,27,""
32,F,SMessageAddress,task,TTask,2,0,2,2,0,0,0,0,0,1,1,0,28,""
```

解析得到 struct_object{SMessageAddress, 4字节, 3个成员, 0个array成员,[object1, object2, object3]}

- object1为第1个字段创建的对象 field_object1{board, TBoard, 类型0, field1_metadata, 字节偏移0, 字段大小1字节}
	- field1_metadata = ""
- object2为第2个字段创建的对象 field_object2{cpu,   TCpu,   类型0, field2_metadata, 字节偏移1, 字段大小1字节}
	- field2_metadata = ""
- object3为第3个字段创建的对象 field_object3{task,  TTask,  类型2, field3_metadata, 字节偏移2, 字段大小2字节}
	- field3_metadata = ""

注：其中的metadata包含了对field_object里面的“类型”所做的解释，由于当前field的类型不为空，说明该类型已经在之前定义，metadata为空。


解析举例2：非自定义类型的字段-默认内建类型的字段（0,1,2,3,4,5,26,27）。

```
34,S,SHeaderFlags,,,17,0,0,2,0,2,2,0,0,0,1,0,0,""
35,F,SHeaderFlags,system,,0,0,0,1,0,0,0,0,0,1,0,0,0,"reserved for transportation/platform layer (checksum etc)"
36,F,SHeaderFlags,user,,0,0,1,1,0,0,0,0,0,1,0,0,0,"reserved for application layer, transported "as is"."
```

解析得到 struct_object{SHeaderFlags, 2字节, 2个成员, 0个array成员,[object1, object2]}

- object1为第1个字段创建的对象 field_object1{system, "", 类型0, field1_metadata, 字节偏移0, 字段大小1字节}
	- field1_metadata = MetadataBasicType("_anon_uint8", 1, "B")
- object2为第2个字段创建的对象 field_object2{user,   "", 类型0, field2_metadata, 字节偏移1, 字段大小1字节}
	- field2_metadata = MetadataBasicType("_anon_uint8", 1, "B")

注：此时field自定义的类型为""，因此需要使用默认后面的类型来进行解析，此时用 metadata来描述，这个例子中是“默认的内建类型”。

解析举例3：非自定义类型的字段-ARRAY（14）。

```
550,S,SConfigurableUsageAddresses,,,17,0,0,196,0,2,3,0,0,0,1,0,0,""
551,F,SConfigurableUsageAddresses,numOfConfigurableUsageAddresses,TNumberOfItems,4,0,0,4,0,0,0,0,0,1,1,0,427,""
552,F,SConfigurableUsageAddresses,configurableUsageAddresses,,14,0,4,192,0,24,0,0,0,1,1,0,0,""
553,F,SConfigurableUsageAddresses,configurableUsageAddresses,SAddressInfo,17,0,0,8,0,2,0,0,0,2,1,0,547,""
```

解析得到 struct_object{SConfigurableUsageAddresses, 196字节, 2个成员, 1个array成员, [object1, object2]}

- object1为第1个字段创建的对象 field_object1{numOfConfigurableUsageAddresses, "TNumberOfItems", 类型4, field1_metadata, 字节偏移0, 字段大小4字节}
	- field1_metadata = ""
- object2为第2个字段创建的对象 field_object2{configurableUsageAddresses,   "", 类型14, field2_metadata, 字节偏移4, 字段大小192字节}
	- field2_metadata = MetadataArray("", 192, 24, "") -- 24个元素。

对于第3行的field的处理分两步：首先，解析出该field的metadata，比如这个例子里是MetadataStruct("SAddressInfo", 8, 2, 0)。然
后再将解析出来的metadata添加到之前已经解析出来的array里的meta，这里是MetadataArray("", 192, 24, "")。

**注：当前实现里对于array的解析结果，这个例子里因为SAddressInfo已经在之前定义，因此array的metadata为None**	

解析举例4：非自定义类型的字段-POINTER（15）。

```
11333,S,TRecoveryFunctionPtr,,,15,0,0,4,0,0,0,0,0,0,0,0,0,""
11334,S,SFaultTypeData,,,17,0,0,40,0,10,10,0,0,0,1,0,0,""
11335,F,SFaultTypeData,faultId,EFaultId,4,1,0,4,0,1709,0,1,0,1,1,0,9602,""
11336,F,SFaultTypeData,faultClass,EFaultClass,4,1,4,4,0,7,0,1,0,1,1,0,11312,""
11337,F,SFaultTypeData,faultIdTotalCounter,TCounter,4,0,8,4,0,0,0,0,0,1,1,0,11320,""
11338,F,SFaultTypeData,blocked,TBoolean,4,0,12,4,0,0,0,0,0,1,1,0,457,""
11339,F,SFaultTypeData,faultDelivery,EFaultDelivery,4,1,16,4,0,5,0,1,0,1,1,0,11321,""
11340,F,SFaultTypeData,faultDetectionWindow,TCounter,4,0,20,4,0,0,0,0,0,1,1,0,11320,""
11341,F,SFaultTypeData,faultIndFrequency,TCounter,4,0,24,4,0,0,0,0,0,1,1,0,11320,""
11342,F,SFaultTypeData,faultIdFilterCounter,TCounter,4,0,28,4,0,0,0,0,0,1,1,0,11320,""
11343,F,SFaultTypeData,recoveryState,ERecoveryState,4,1,32,4,0,5,0,1,0,1,1,0,11327,""
11344,F,SFaultTypeData,recoveryFunctionPtr,TRecoveryFunctionPtr,15,0,36,4,0,0,0,0,0,1,1,0,11333,""
```

对于这些非自定义类型的字段，都会在前面预先定义。比如在 SFaultTypeData（11334） 里有 recoveryFunctionPtr（11344）它会预先
定义好该字段的类型 TRecoveryFunctionPtr （11333）。

解析得到 struct_object{SFaultTypeData, 40字节, 10个成员, 0个array成员, [object1, object2......object10]}

- object1: field_object1{faultId, "EFaultId", 类型4, field1_metadata, 字节偏移0, 字段大小4字节}
	- field1_metadata = None
- object2: field_object2{faultClass, "EFaultClass", 类型4, field2_metadata, 字节偏移4, 字段大小4字节}
	- field2_metadata = None
- object3: field_object3{faultIdTotalCounter, "TCounter", 类型4, field3_metadata, 字节偏移8, 字段大小4字节}
	- field3_metadata = None
- object4: field_object4{blocked, "TBoolean", 类型4, field4_metadata, 字节偏移12, 字段大小4字节}
	- field4_metadata = None
- object5: field_object5{faultDelivery, "EFaultDelivery", 类型4, field5_metadata, 字节偏移16, 字段大小4字节}
	- field5_metadata = None
- object6: field_object6{faultDetectionWindow, "TCounter", 类型4, field6_metadata, 字节偏移20, 字段大小4字节}
	- field6_metadata = None
- object7: field_object7{faultIndFrequency, "TCounter", 类型4, field7_metadata, 字节偏移24, 字段大小4字节}
	- field7_metadata = None
- object8: field_object8{faultIdFilterCounter, "TCounter", 类型4, field8_metadata, 字节偏移28, 字段大小4字节}
	- field8_metadata = None
- object9: field_object9{recoveryState, "ERecoveryState", 类型4, field9_metadata, 字节偏移32, 字段大小4字节}
	- field9_metadata = None
- object10: field_object10{recoveryFunctionPtr, "TRecoveryFunctionPtr", 类型15, field10_metadata, 字节偏移36, 字段大小4字节}
	- field10_metadata = None


解析举例5：非自定义类型的字段-STRUCT（17）。

```
37,S,SMessageHeader,,,17,0,0,16,0,5,5,0,0,0,1,0,0,""
38,F,SMessageHeader,id,TMessageId,4,0,0,4,0,0,0,0,0,1,1,0,25,""
39,F,SMessageHeader,receiver,SMessageAddress,17,0,4,4,0,3,0,0,0,1,1,0,29,""
40,F,SMessageHeader,sender,SMessageAddress,17,0,8,4,0,3,0,0,0,1,1,0,29,""
41,F,SMessageHeader,length,TMsgLength,2,0,12,2,0,0,0,0,0,1,1,0,33,""
42,F,SMessageHeader,flags,SHeaderFlags,17,0,14,2,0,2,0,0,0,1,1,0,34,""
```

解析得到 struct_object{SMessageHeader, 16字节, 5个成员, 5个array成员, [object1, object2......object4]}

- object1: field_object1{id, "TMessageId", 类型4, field1_metadata, 字节偏移0, 字段大小4字节}
	- field1_metadata = None
- object2: field_object2{receiver, "SMessageAddress", 类型17, field2_metadata, 字节偏移4, 字段大小4字节}
	- field2_metadata = None
- object3: field_object3{sender, "SMessageAddress", 类型17, field3_metadata, 字节偏移8, 字段大小4字节}
	- field3_metadata = None
- object4: field_object4{length, "TMsgLength", 类型2, field4_metadata, 字节偏移12, 字段大小2字节}
	- field4_metadata = None
- object5: field_object5{flags, "SHeaderFlags", 类型17, field5_metadata, 字节偏移14, 字段大小2字节}
	- field5_metadata = None

解析举例6：非自定义类型的字段-UNION（18）。

```
815,S,UWmpDcmCaParamsContainer,,,17,0,0,1804,0,2,2,0,0,0,1,0,0,""
816,F,UWmpDcmCaParamsContainer,discriminator,EDiscUWmpDcmCaParamsContainer,4,1,0,4,0,2,0,1,0,1,1,0,505,""
817,F,UWmpDcmCaParamsContainer,u,UInnerUWmpDcmCaParamsContainer,18,0,4,1800,0,2,0,0,0,1,1,0,812,""
```

解析得到 struct_object{UWmpDcmCaParamsContainer, 1804字节, 2个成员, 0个array成员, [object1, object2]}

- object1: field_object1{discriminator, "EDiscUWmpDcmCaParamsContainer", 类型4, field1_metadata, 字节偏移0, 字段大小4字节}
	- field1_metadata = None
- object2: field_object2{u, "UInnerUWmpDcmCaParamsContainer", 类型18, field2_metadata, 字节偏移4, 字段大小1800字节}
	- field2_metadata = None
				
				
4. 类型D

-  第0项：行序号。
-  第1项：行类型，定义为消息，固定为D。
-  第2项：数据类型，消息ID。
-  第3项：
-  第4项：消息名称。
-  第5项：tag
-  第6项：tag描述
-  第7项：
-  第8项：大小
-  第9项：
- 第10项：消息结构包含的成员数量
- 第11项：消息结构包含的成员数量（额外计算数组成员）
- 第12项：
- 第13项：
- 第14项：
- 第15项：
- 第16项：
- 第17项：

类型D定义消息。

   927,    D,    43CF,    ,    PS_CA_PUCCH_RESOURCES_REQ_MSG,    23,    0,    0,    52,    0,    12,    13,    0,    0,    0,    1,    0,    0,    ""
    0,     1,       2,   3,                                4,     5,    6,    7,     8,    9,    10,    11,   12,   13,   14,   15,   16,   17,    18
order,  line  message     ,                     message name,      ,     ,     ,  size,     , field extra f
        type,      id,                                                                       number,number,
		
		
5. 类型M

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

类型M作为D类型的字段使用。

   928,    M,    43CF,    msgHeader,    SMessageHeader,    17,    0,    0,    16,    0,    5,    0,    0,    0,    1,    1,    0,    37,    ""
     0,    1,       2,            3,                 4,     5,    6,    7,     8,    9,   10,   11,   12,   13,   14,   15,   16,    17,    18
order,  line  message    field name,        field type,      ,     , byte   size,     ,     ,     ,     ,     ,     ,     ,     ,      ,
        type,      id,                                             offset,


		
解析举例1：自定义的类型的字段。

```
43,D,29E1,,TEST_BB_FETCH_TRACE_REQ_MSG,23,0,0,20,0,2,2,0,0,0,1,0,0,""
44,M,29E1,msgHeader,SMessageHeader,17,0,0,16,0,5,0,0,0,1,1,0,37,""
45,M,29E1,spare,,4,0,16,4,0,0,0,0,0,1,0,0,0,""
```

解析得到 struct_object{29E1, TEST_BB_FETCH_TRACE_REQ_MSG, 20字节, 2个成员, 0个array成员,[object1, object2}

- object1为第1个字段创建的对象 field_object1{msgHeader, SMessageHeader, 类型17, field1_metadata, 字节偏移0, 字段大小16字节}
	- field1_metadata = ""
- object2为第2个字段创建的对象 field_object2{spare,   "",   类型4, field2_metadata, 字节偏移16, 字段大小4字节}
	- field2_metadata = ""


注：其中的metadata包含了对field_object里面的“类型”所做的解释，由于当前field的类型不为空，说明该类型已经在之前定义，metadata为空。

解析举例2：包含有ARRAY的字段。

```
74,D,4E49,,PHY_NB_PBCH_SEND_REQ_MSG,23,0,0,48,0,9,11,0,0,0,1,0,0,""
75,M,4E49,msgHeader,SMessageHeader,17,0,0,16,0,5,0,0,0,1,1,0,37,""
76,M,4E49,lnCelId,TCellId,4,0,16,4,0,0,0,0,0,1,1,0,69,""
77,M,4E49,frameNumber,TFrameNumber,4,0,20,4,0,0,0,0,0,1,1,0,70,""
78,M,4E49,subFrameNumber,TSubFrameNumber,4,0,24,4,0,0,0,0,0,1,1,0,71,""
79,M,4E49,sfnSubCellId,,0,0,28,1,0,0,0,0,0,1,0,0,0,""
80,M,4E49,padding,,14,0,29,3,0,3,0,0,0,1,1,0,0,""
81,M,4E49,padding,,0,0,0,1,0,0,0,0,0,2,0,0,0,""
82,M,4E49,txPower,TTxPower,5,0,32,4,0,0,0,0,0,1,1,0,72,""
83,M,4E49,tbSize,TTbSize,4,0,36,4,0,0,0,0,0,1,1,0,73,""
84,M,4E49,data,,14,0,40,8,0,8,0,0,0,1,1,0,0,""
85,M,4E49,data,,0,0,0,1,0,0,0,0,0,2,0,0,0,""
```

解析得到 struct_object{4E49, PHY_NB_PBCH_SEND_REQ_MSG, 48字节, 9个成员, 2个array成员, [object1, object2...object9]}

- object1为第1个字段创建的对象 field_object1{msgHeader, "SMessageHeader", 类型17, field1_metadata, 字节偏移0, 字段大小16字节}
	- field1_metadata = ""
- object2为第2个字段创建的对象 field_object2{lnCelId, "TCellId", 类型4, field2_metadata, 字节偏移16, 字段大小4字节}
	- field2_metadata = ""
- object3为第3个字段创建的对象 field_object3{frameNumber, "TFrameNumber", 类型4, field3_metadata, 字节偏移20, 字段大小4字节}
	- field3_metadata = ""
- object4为第4个字段创建的对象 field_object4{subFrameNumber, "TSubFrameNumber", 类型4, field4_metadata, 字节偏移24, 字段大小4字节}
	- field4_metadata = ""
- object5为第5个字段创建的对象 field_object5{sfnSubCellId, "", 类型0, field5_metadata, 字节偏移28, 字段大小1字节}
	- field5_metadata = ""
- object6为第6个字段创建的对象 field_object6{padding, "", 类型14, field6_metadata, 字节偏移29, 字段大小3字节}
	- field6_metadata = MetadataArray("", 192, 24, "") -- 24个元素。
- object7为第7个字段创建的对象 field_object7{txPower, "TTxPower", 类型5, field7_metadata, 字节偏移32, 字段大小4字节}
	- field7_metadata = ""
- object8为第8个字段创建的对象 field_object8{tbSize, "TTbSize", 类型4, field8_metadata, 字节偏移36, 字段大小4字节}
	- field8_metadata = ""
- object9为第9个字段创建的对象 field_object9{data, "", 类型14, field9_metadata, 字节偏移40, 字段大小8字节}
	- field9_metadata = MetadataArray("", 192, 24, "") -- 24个元素。

对于数组的定义分成了两行来进行，第 14 列定义递归层次：
	- 80,M,4E49,padding,,14,0,29,3,0,3,0,0,0,1,1,0,0,""
		- 层次为1的时候解析 ARRAY field vs 整个消息 的联系。
		- 创建 ARRAY 的 metadata。
		- 将 metadata 写入 PHY_NB_PBCH_SEND_REQ_MSG。
		
	- 81,M,4E49,padding,,0,0,0,1,0,0,0,0,0,2,0,0,0,""
		- 层次为2的时候解析 ARRAY vs ARRAY元素  的联系。
		- 创建 ARRAY元素 的 metadata。
		- 将 metadata 写入 ARRAY metadata 里面。
	
对于第3行的field的处理分两步：首先，解析出该field的metadata，比如这个例子里是MetadataStruct("SAddressInfo", 8, 2, 0)。然
后再将解析出来的metadata添加到之前已经解析出来的array里的meta，这里是MetadataArray("", 192, 24, "")。

**注：当前实现里对于array的解析结果，这个例子里因为SAddressInfo已经在之前定义，因此array的metadata为None**	
		