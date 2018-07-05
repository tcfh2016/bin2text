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
        self.object._parse_struct(items)
        #print self.object._metadata["SMessageAddress"]

        expect_meta = metadata.MetadataStruct("SMessageAddress", 4, 3, 0)
        print expect_meta
        self.assertEqual(self.object._metadata["SMessageAddress"], expect_meta)

if __name__ == '__main__':
    unittest.main()
