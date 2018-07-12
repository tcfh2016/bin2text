# -*- coding: utf-8 -*-

import unittest

import src.metadata_handler as handler
import src.metadata as metadata

class MetaDataHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.object = handler.MetaDataHandler("", "")

    def test_valid_items(self):
        self.assertFalse(self.object._valid_items([1,2]))
        self.assertTrue(self.object._valid_items([48,'C',"EInetRouteOperation","EInetRouteOperation_Last","",4,7,0,0,0,6,0,0,0,1,0,0,0,""]))


    def test_parse_struct(self):
        items = [29,'S',"SMessageAddress","","",17,0,0,4,0,3,3,0,0,0,1,0,0,""]
        self.object._parse_item(items)

        expect_meta = metadata.MetadataStruct("SMessageAddress", 4, 3, 0)
        self.assertEqual(self.object._metadata["SMessageAddress"], expect_meta)

    def test_parse_struct_with_defined_datastructure_fields(self):
        s = [29,'S',"SMessageAddress","","",17,0,0,4,0,3,3,0,0,0,1,0,0,""]
        f1 = [30,'F',"SMessageAddress","board","TBoard",0,0,0,1,0,0,0,0,0,1,1,0,26,""]
        f2 = [31,'F',"SMessageAddress","cpu","TCpu",0,0,1,1,0,0,0,0,0,1,1,0,27,""]
        f3 = [32,'F',"SMessageAddress","task","TTask",2,0,2,2,0,0,0,0,0,1,1,0,28,""]

        map(lambda x:self.object._parse_item(x), [s, f1, f2, f3])

        self.assertEqual(self.object._metadata["SMessageAddress"]._parsed_field_counter,
                         self.object._metadata["SMessageAddress"]._field_number)
        self.assertEqual(len(self.object._metadata["SMessageAddress"]._fields), 3)

    def test_parse_struct_with_default_datastructure_fields(self):
        s = [34,'S',"SHeaderFlags","","",17,0,0,2,0,2,2,0,0,0,1,0,0,""]
        f1 = [35,'F',"SHeaderFlags","system","",0,0,0,1,0,0,0,0,0,1,0,0,0,"reserved for transportation/platform layer (checksum etc)"]
        f2 = [36,'F',"SHeaderFlags","user","",0,0,1,1,0,0,0,0,0,1,0,0,0,"reserved for application layer, transported as is."]

        map(lambda x:self.object._parse_item(x), [s, f1, f2])

        self.assertEqual(self.object._metadata["SHeaderFlags"]._parsed_field_counter,
                         self.object._metadata["SHeaderFlags"]._field_number)
        self.assertEqual(len(self.object._metadata["SHeaderFlags"]._fields), 2)
        self.assertEqual(self.object._metadata["SHeaderFlags"]._fields[0]._metadata, metadata.MetadataBasicType(f1[5]))

    def test_parse_struct_with_array_fields(self):
        s = [550,'S',"SConfigurableUsageAddresses","","",17,0,0,196,0,2,3,0,0,0,1,0,0,""]
        f1 = [551,'F',"SConfigurableUsageAddresses","numOfConfigurableUsageAddresses","TNumberOfItems",4,0,0,4,0,0,0,0,0,1,1,0,427,""]
        f2 = [552,'F',"SConfigurableUsageAddresses","configurableUsageAddresses","",14,0,4,192,0,24,0,0,0,1,1,0,0,""]
        f3 = [553,'F',"SConfigurableUsageAddresses","configurableUsageAddresses","SAddressInfo",17,0,0,8,0,2,0,0,0,2,1,0,547,""]

        map(lambda x:self.object._parse_item(x), [s, f1, f2, f3])

        self.assertEqual(self.object._metadata["SConfigurableUsageAddresses"]._parsed_field_counter,
                         self.object._metadata["SConfigurableUsageAddresses"]._field_number)
        self.assertEqual(len(self.object._metadata["SConfigurableUsageAddresses"]._fields), 2)

        expected_array = metadata.MetadataArray("", 192, 24, None)
        #expected_array._element_metadata = metadata.MetadataStruct("", 192, 24, None)
        self.assertEqual(self.object._metadata["SConfigurableUsageAddresses"]._fields[1]._metadata, expected_array)

    def test_parse_struct_with_pointer_fields(self):
        s = [11334,'S',"SFaultTypeData","","",17,0,0,40,0,10,10,0,0,0,1,0,0,""]
        f1 = [11335,'F',"SFaultTypeData","faultId","EFaultId",4,1,0,4,0,1709,0,1,0,1,1,0,9602,""]
        f2 = [11336,'F',"SFaultTypeData","faultClass","EFaultClass",4,1,4,4,0,7,0,1,0,1,1,0,11312,""]
        f3 = [11337,'F',"SFaultTypeData","faultIdTotalCounter","TCounter",4,0,8,4,0,0,0,0,0,1,1,0,11320,""]
        f4 = [11338,'F',"SFaultTypeData","blocked","TBoolean",4,0,12,4,0,0,0,0,0,1,1,0,457,""]
        f5 = [11339,'F',"SFaultTypeData","faultDelivery","EFaultDelivery",4,1,16,4,0,5,0,1,0,1,1,0,11321,""]
        f6 = [11340,'F',"SFaultTypeData","faultDetectionWindow","TCounter",4,0,20,4,0,0,0,0,0,1,1,0,11320,""]
        f7 = [11341,'F',"SFaultTypeData","faultIndFrequency","TCounter",4,0,24,4,0,0,0,0,0,1,1,0,11320,""]
        f8 = [11342,'F',"SFaultTypeData","faultIdFilterCounter","TCounter",4,0,28,4,0,0,0,0,0,1,1,0,11320,""]
        f9 = [11343,'F',"SFaultTypeData","recoveryState","ERecoveryState",4,1,32,4,0,5,0,1,0,1,1,0,11327,""]
        f10 = [11344,'F',"SFaultTypeData","recoveryFunctionPtr","TRecoveryFunctionPtr",15,0,36,4,0,0,0,0,0,1,1,0,11333,""]

        map(lambda x:self.object._parse_item(x), [s, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10])

        self.assertEqual(self.object._metadata["SFaultTypeData"]._parsed_field_counter,
                         self.object._metadata["SFaultTypeData"]._field_number)
        self.assertEqual(len(self.object._metadata["SFaultTypeData"]._fields), 10)

        expected_field = metadata.Field(9,"recoveryFunctionPtr", "TRecoveryFunctionPtr", 15, None, 36, 4)        
        self.assertEqual(self.object._metadata["SFaultTypeData"]._fields[9], expected_field)

if __name__ == '__main__':
    unittest.main()
