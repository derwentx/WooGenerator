from os import sys, path
import random
# import unittest
import traceback
from unittest import main  # , skip, TestCase
# from tabulate import tabulate
from bisect import insort

if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from testSyncClient import abstractSyncClientTestCase
from context import woogenerator
from woogenerator.utils import TimeUtils, Registrar, SanitationUtils
from woogenerator.sync_client_user import UsrSyncClientWP
from woogenerator.coldata import ColDataUser
from woogenerator.parsing.user import CsvParseUser, CsvParseUserApi  # , ImportUser
# , CardMatcher, NocardEmailMatcher, EmailMatcher
from woogenerator.matching import UsernameMatcher, MatchList
from woogenerator.syncupdate import SyncUpdate, SyncUpdateUsrApi


class testUsrSyncUpdate(abstractSyncClientTestCase):
    # yaml_path = "merger_config.yaml"
    optionNamePrefix = 'test_'

    def __init__(self, *args, **kwargs):
        super(testUsrSyncUpdate, self).__init__(*args, **kwargs)
        self.SSHTunnelForwarderParams = {}
        self.PyMySqlconnect_params = {}
        self.jsonconnect_params = {}
        self.actconnect_params = {}
        self.actDbParams = {}
        self.fs_params = {}

    def processConfig(self, config):
        wp_srv_offset = config.get(self.optionNamePrefix + 'wp_srv_offset', 0)
        wp_api_key = config.get(self.optionNamePrefix + 'wp_api_key')
        wp_api_secret = config.get(self.optionNamePrefix + 'wp_api_secret')
        store_url = config.get(self.optionNamePrefix + 'store_url', '')
        wp_user = config.get(self.optionNamePrefix + 'wp_user')
        wp_pass = config.get(self.optionNamePrefix + 'wp_pass')
        wp_callback = config.get(self.optionNamePrefix + 'wp_callback')
        merge_mode = config.get('merge_mode', 'sync')
        master_name = config.get('master_name', 'MASTER')
        slave_name = config.get('slave_name', 'SLAVE')
        default_last_sync = config.get('default_last_sync')

        TimeUtils.set_wp_srv_offset(wp_srv_offset)
        SyncUpdate.set_globals(master_name, slave_name,
                               merge_mode, default_last_sync)

        self.wpApiParams = {
            'api_key': wp_api_key,
            'api_secret': wp_api_secret,
            'url': store_url,
            'wp_user': wp_user,
            'wp_pass': wp_pass,
            'callback': wp_callback
        }

        # Registrar.DEBUG_UPDATE = True

    def setUp(self):
        super(testUsrSyncUpdate, self).setUp()

        for var in ['wpApiParams']:
            print var, getattr(self, var)

        Registrar.DEBUG_API = True

    def testUploadSlaveChanges(self):

        maParser = CsvParseUser(
            cols=ColDataUser.get_act_import_cols(),
            defaults=ColDataUser.get_defaults()
        )

        master_bus_type = "Salon"
        master_client_grade = str(random.random())
        master_uname = "neil"

        master_data = [map(unicode, row) for row in [
            ["E-mail", "Role", "First Name", "Surname", "Nick Name", "Contact", "Client Grade", "Direct Brand", "Agent", "Birth Date", "Mobile Phone", "Fax", "Company", "Address 1", "Address 2", "City", "Postcode", "State", "Country", "Phone", "Home Address 1", "Home Address 2", "Home City",
                "Home Postcode", "Home Country", "Home State", "MYOB Card ID", "MYOB Customer Card ID", "Web Site", "ABN", "Business Type", "Referred By", "Lead Source", "Mobile Phone Preferred", "Phone Preferred", "Personal E-mail", "Edited in Act", "Wordpress Username", "display_name", "ID", "updated"],
            ["neil@technotan.com.au", "ADMIN", "Neil", "Cunliffe-Williams", "Neil Cunliffe-Williams", "", master_client_grade, "TT", "", "", +61416160912, "", "Laserphile", "7 Grosvenor Road", "", "Bayswater", 6053, "WA",
                "AU", "0416160912", "7 Grosvenor Road", "", "Bayswater", 6053, "AU", "WA", "", "", "http://technotan.com.au", 32, master_bus_type, "", "", "", "", "", "", master_uname, "Neil", 1, "2015-07-13 22:33:05"]
        ]]

        maParser.analyse_rows(master_data)

        print "MASTER RECORDS: \n", maParser.tabulate()

        saParser = CsvParseUserApi(
            cols=ColDataUser.get_wp_import_cols(),
            defaults=ColDataUser.get_defaults()
        )

        with UsrSyncClientWP(self.wpApiParams) as slaveClient:
            slaveClient.analyse_remote(saParser, search=master_uname)

        print "SLAVE RECORDS: \n", saParser.tabulate()

        updates = []
        globalMatches = MatchList()

        # Matching
        usernameMatcher = UsernameMatcher()
        usernameMatcher.process_registers(
            saParser.usernames, maParser.usernames)
        globalMatches.add_matches(usernameMatcher.pure_matches)

        print "username matches (%d pure)" % len(usernameMatcher.pure_matches)

        sync_cols = ColDataUser.get_sync_cols()

        for count, match in enumerate(globalMatches):
            m_object = match.m_objects[0]
            s_object = match.s_objects[0]

            syncUpdate = SyncUpdateUsrApi(m_object, s_object)
            syncUpdate.update(sync_cols)

            print "SyncUpdate: ", syncUpdate.tabulate()

            if not syncUpdate:
                continue

            if syncUpdate.s_updated:
                insort(updates, syncUpdate)

        slaveFailures = []

        #
        response_json = {}

        with UsrSyncClientWP(self.wpApiParams) as slaveClient:

            for count, update in enumerate(updates):
                try:
                    response = update.update_slave(slaveClient)
                    print "response (code) is %s" % response
                    assert response, "response should exist because update should not be empty. update: %s" % update.tabulate(
                        tablefmt="html")
                    if response:
                        print "response text: %s" % response.text
                        response_json = response.json()

                except Exception as exc:
                    slaveFailures.append({
                        'update': update,
                        'master': SanitationUtils.coerce_unicode(update.new_m_object),
                        'slave': SanitationUtils.coerce_unicode(update.new_s_object),
                        'mchanges': SanitationUtils.coerce_unicode(update.get_master_updates()),
                        'schanges': SanitationUtils.coerce_unicode(update.get_slave_updates()),
                        'exception': repr(exc)
                    })
                    Registrar.register_error("ERROR UPDATING SLAVE (%s): %s\n%s" % (
                        update.slave_id,
                        repr(exc),
                        traceback.format_exc()
                    ))

        self.assertTrue(response_json.get('meta'))
        self.assertEqual(response_json.get('meta', {}).get(
            'business_type'), master_bus_type)
        self.assertEqual(response_json.get('meta', {}).get(
            'client_grade'), master_client_grade)


if __name__ == '__main__':
    main()