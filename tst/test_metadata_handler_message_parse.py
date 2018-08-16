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
'''
    def test_parse_struct_with_defined_datastructure_fields(self):
        s = [29,'S',"SMessageAddress","","",17,0,0,4,0,3,3,0,0,0,1,0,0,""]
        f1 = [30,'F',"SMessageAddress","board","TBoard",0,0,0,1,0,0,0,0,0,1,1,0,26,""]
        f2 = [31,'F',"SMessageAddress","cpu","TCpu",0,0,1,1,0,0,0,0,0,1,1,0,27,""]
        f3 = [32,'F',"SMessageAddress","task","TTask",2,0,2,2,0,0,0,0,0,1,1,0,28,""]

        map(lambda x:self.object._parse_item(x), [s, f1, f2, f3])

        self.assertEqual(self.object._metadata["SMessageAddress"]._parsed_field_counter,
                         self.object._metadata["SMessageAddress"]._field_number)
        self.assertEqual(len(self.object._metadata["SMessageAddress"]._fields), 3)
'''
if __name__ == '__main__':
    unittest.main()
