from __future__ import print_function
import os
from unittest import TestCase, main, skip, TestSuite, TextTestRunner
import argparse

from context import woogenerator
from woogenerator.coldata import ColDataWoo
from woogenerator.parsing.woo import ImportWooProduct, CsvParseWoo, CsvParseTT, WooProdList
from woogenerator.utils import TimeUtils, Registrar, SanitationUtils
from woogenerator.utils import (HtmlReporter, ProgressCounter, Registrar,
                                SanitationUtils, TimeUtils, DebugUtils)
from woogenerator.config import (ArgumentParserProd, ArgumentParserProtoProd,
                                 SettingsNamespaceProd, init_settings)
from woogenerator.generator import populate_master_parsers, init_registrar

from context import tests_datadir

class TestGenerator(TestCase):
    def setUp(self):

        self.settings = SettingsNamespaceProd()
        self.settings.local_work_dir = tests_datadir
        self.settings.local_live_config = None
        self.settings.local_test_config = "generator_config_test.yaml"
        self.settings.download_master = False
        self.settings.master_file = os.path.join(tests_datadir, "generator_sample.csv")
        # self.config_path = os.path.join(tests_datadir, "generator_config_test.yaml")
        self.override_args = ""
        # self.override_args = "--skip-download-master"

    def test_init_settings(self):
        Registrar.DEBUG_MESSAGE = True
        Registrar.DEBUG_ERROR = True
        self.settings = init_settings(
            settings=self.settings,
            override_args=self.override_args,
            argparser_class=ArgumentParserProd
        )
        self.assertEqual(self.settings.master_name, "GDrive")
        self.assertEqual(self.settings.slave_name, "WooCommerce")
        self.assertEqual(self.settings.merge_mode, "sync")
        self.assertEqual(self.settings.schema, "WC")
        self.assertEqual(self.settings.download_master, False)


    def test_populate_master_parsers(self):
        self.test_init_settings()
        self.parsers = argparse.Namespace()
        # self.settings.product_parser_args = {
        #     'import_name': self.settings.import_name,
        #     'item_depth': self.settings.item_depth,
        #     'taxo_depth': self.settings.taxo_depth,
        # }

        self.parsers = populate_master_parsers(
            self.parsers,
            self.settings
        )

        print(getattr(self.parsers, 'ma').tabulate())


if __name__ == '__main__':
    main()
