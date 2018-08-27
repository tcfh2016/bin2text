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

    def test_parse_message_with_defined_datastructure_fields(self):
        m = [43,'D',"29E1","","TEST_BB_FETCH_TRACE_REQ_MSG",23,0,0,20,0,2,2,0,0,0,1,0,0,""]
        f1 = [44,'M',"29E1","msgHeader","SMessageHeader",17,0,0,16,0,5,0,0,0,1,1,0,37,""]
        f2 = [45,'M',"29E1","spare","",4,0,16,4,0,0,0,0,0,1,0,0,0,""]

        map(lambda x:self.object._parse_item(x), [m, f1, f2])

        self.assertEqual(self.object._metadata_message[0x29E1]._parsed_field_counter,
                         self.object._metadata_message[0x29E1]._field_number)
        self.assertEqual(len(self.object._metadata_message[0x29E1]._fields), 2)

if __name__ == '__main__':
    unittest.main()
