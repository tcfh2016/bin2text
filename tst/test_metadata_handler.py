# -*- coding: utf-8 -*-

import unittest

import src.metadata_handler as handler

class MetaDataHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.object = handler.MetaDataHandler("", "")

    def test_valid_items(self):
        self.assertFalse(self.object._valid_items([1,2]))
        self.assertTrue(self.object._valid_items([48,'C',"EInetRouteOperation","EInetRouteOperation_Last","",4,7,0,0,0,6,0,0,0,1,0,0,0,""]))



if __name__ == '__main__':
    unittest.main()
