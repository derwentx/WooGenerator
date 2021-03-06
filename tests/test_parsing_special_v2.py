import os
import time
import unittest

from context import get_testdata, TESTS_DATA_DIR, woogenerator
from woogenerator.parsing.special import CsvParseSpecial
from woogenerator.utils import Registrar, TimeUtils


class TestCSVParseSpecialV2(unittest.TestCase):

    def setUp(self):
        # import_name = TimeUtils.get_ms_timestamp()

        self.spec_path = os.path.join(TESTS_DATA_DIR, "specials_v2.csv")

        self.special_parser_args = {
            # 'import_name':import_name
        }

        Registrar.DEBUG_ERROR = False
        Registrar.DEBUG_WARN = False
        Registrar.DEBUG_MESSAGE = False

        # Registrar.DEBUG_MESSAGE = True
        # Registrar.DEBUG_SPECIAL = True
        # Registrar.DEBUG_PARSER = True

    def test_basic(self):
        special_parser = CsvParseSpecial(
            **self.special_parser_args
        )


        special_parser.analyse_file(self.spec_path)

        if Registrar.DEBUG_PARSER:
            Registrar.register_message("number of special groups: %s" \
                                       % len(special_parser.rule_groups))
            Registrar.register_message("number of special rules: %s" % len(special_parser.rules))
            Registrar.register_message(special_parser.tabulate(tablefmt="simple"))

        # check that loner has correct ending
        is_singular_child = False
        for index, special in special_parser.rule_groups.items():
            if len(special.children) == 1:
                is_singular_child = True
                child = special.children[0]
                self.assertEqual(index, child.index)
        self.assertTrue(is_singular_child)

    def test_has_happened_yet(self):
        special_parser = CsvParseSpecial(
            **self.special_parser_args
        )

        special_parser.analyse_file(self.spec_path)

        TimeUtils.set_override_time(time.strptime(
            "2018-01-01", TimeUtils.wp_date_format))

        eofy_special = special_parser.rule_groups.get('EOFY2016')
        eofy_start_time = TimeUtils.datetime2utctimestamp(eofy_special.start_time)
        self.assertLess(eofy_start_time, TimeUtils.current_tsecs())
        self.assertTrue(eofy_special.has_started)
        self.assertTrue(eofy_special.has_finished)
        self.assertFalse(eofy_special.is_active)

    def test_determine_groups(self):
        special_parser = CsvParseSpecial(
            **self.special_parser_args
        )

        special_parser.analyse_file(self.spec_path)

        # Registrar.DEBUG_SPECIAL = True
        # Registrar.DEBUG_MESSAGE = True

        override_groups = special_parser.determine_current_spec_grps(
            'override',
            'EOFY2016'
        )
        self.assertEquals(
            override_groups, [special_parser.rule_groups.get('EOFY2016')])

        TimeUtils.set_override_time(time.strptime(
            "2018-01-01", TimeUtils.wp_date_format))

        auto_next_groups = special_parser.determine_current_spec_grps(
            'auto_next'
        )
        self.assertEquals(auto_next_groups, [])

        TimeUtils.set_override_time(time.strptime(
            "2016-08-11", TimeUtils.wp_date_format))

        auto_next_groups = special_parser.determine_current_spec_grps(
            'auto_next'
        )
        self.assertEquals(
            auto_next_groups, [special_parser.rule_groups.get('SP2016-08-12')])

        TimeUtils.set_override_time(time.strptime(
            "2016-06-11", TimeUtils.wp_date_format))

        auto_next_groups = special_parser.determine_current_spec_grps(
            'auto_next'
        )
        self.assertEquals(
            auto_next_groups, [special_parser.rule_groups.get('EOFY2016')])

        TimeUtils.set_override_time(time.strptime(
            "2016-06-13", TimeUtils.wp_date_format))

        auto_next_groups = special_parser.determine_current_spec_grps(
            'auto_next'
        )
        self.assertEquals(
            auto_next_groups, [special_parser.rule_groups.get('EOFY2016')])


if __name__ == '__main__':
    unittest.main()
