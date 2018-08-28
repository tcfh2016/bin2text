# -*- coding: utf-8 -*-

import unittest

import src.metadata_handler as handler
import src.metadata as metadata

class MetaDataHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.object = handler.MetaDataHandler("", "")

    def test_parse_message(self):
        items = [927,'D',"43CF","","PS_CA_PUCCH_RESOURCES_REQ_MSG",23,0,0,52,0,12,13,0,0,0,1,0,0,""]
        self.object._parse_item(items)

        expect_meta = metadata.MetadataMessage("43CF", "PS_CA_PUCCH_RESOURCES_REQ_MSG", 52, 12, 1)
        self.assertEqual(self.object._metadata_message[0x43CF], expect_meta)

    def test_parse_message_with_1_level_fields(self):
        m = [43,'D',"29E1","","TEST_BB_FETCH_TRACE_REQ_MSG",23,0,0,20,0,2,2,0,0,0,1,0,0,""]
        f1 = [44,'M',"29E1","msgHeader","SMessageHeader",17,0,0,16,0,5,0,0,0,1,1,0,37,""]
        f2 = [45,'M',"29E1","spare","",4,0,16,4,0,0,0,0,0,1,0,0,0,""]

        map(lambda x:self.object._parse_item(x), [m, f1, f2])

        self.assertEqual(self.object._metadata_message[0x29E1]._parsed_field_counter,
                         self.object._metadata_message[0x29E1]._field_number)
        self.assertEqual(len(self.object._metadata_message[0x29E1]._fields), 2)

    def test_parse_message_with_2_level_array_fields(self):
        m = [74,'D',"4E49","","PHY_NB_PBCH_SEND_REQ_MSG",23,0,0,48,0,9,11,0,0,0,1,0,0,""]
        f1 = [75,'M',"4E49","msgHeader","SMessageHeader",17,0,0,16,0,5,0,0,0,1,1,0,37,""]
        f2 = [76,'M',"4E49","lnCelId","TCellId",4,0,16,4,0,0,0,0,0,1,1,0,69,""]
        f3 = [77,'M',"4E49","frameNumber","TFrameNumber",4,0,20,4,0,0,0,0,0,1,1,0,70,""]
        f4 = [78,'M',"4E49","subFrameNumber","TSubFrameNumber",4,0,24,4,0,0,0,0,0,1,1,0,71,""]
        f5 = [79,'M',"4E49","sfnSubCellId","",0,0,28,1,0,0,0,0,0,1,0,0,0,""]
        f6 = [80,'M',"4E49","padding","",14,0,29,3,0,3,0,0,0,1,1,0,0,""]
        f7 = [81,'M',"4E49","padding","",0,0,0,1,0,0,0,0,0,2,0,0,0,""]
        f8 = [82,'M',"4E49","txPower","TTxPower",5,0,32,4,0,0,0,0,0,1,1,0,72,""]
        f9 = [83,'M',"4E49","tbSize","TTbSize",4,0,36,4,0,0,0,0,0,1,1,0,73,""]
        f10 = [84,'M',"4E49","data","",14,0,40,8,0,8,0,0,0,1,1,0,0,""]
        f11 = [85,'M',"4E49","data","",0,0,0,1,0,0,0,0,0,2,0,0,0,""]

        map(lambda x:self.object._parse_item(x), [m, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11])

        self.assertEqual(self.object._metadata_message[0x4E49]._parsed_field_counter,
                         self.object._metadata_message[0x4E49]._field_number)
        self.assertEqual(len(self.object._metadata_message[0x4E49]._fields), 9)

if __name__ == '__main__':
    unittest.main()
