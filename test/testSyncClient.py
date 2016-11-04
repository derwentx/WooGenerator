from os import sys, path
import unittest
from unittest import TestCase, main, skip

if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from source.sync_client import *
from source.sync_client_prod import *
from source.sync_client_user import *
from source.coldata import ColData_User, ColData_Woo
from source.csvparse_flat import ImportUser

class abstractSyncClientTestCase(TestCase):
    yamlPath = "generator_config.yaml"
    optionNamePrefix = 'test_'
    # optionNamePrefix = ''

    def processConfig(self, config): raise NotImplementedError()

    def setUp(self):
        try:
            #if you can't stat source
            os.stat('source')
        except OSError:
            #then you must be in source
            tail = os.path.split(os.getcwd())[1]
            assert tail == 'source'
        else:
            #else pls go to source
            os.chdir('source')

        self.importName = TimeUtils.getMsTimeStamp()

        with open(self.yamlPath) as stream:
            config = yaml.load(stream)
            self.processConfig(config)

        Registrar.DEBUG_PROGRESS = True
        Registrar.DEBUG_MESSAGE = True
        Registrar.DEBUG_ERROR = True
        Registrar.DEBUG_WARN = True


class testSyncClient(abstractSyncClientTestCase):
    optionNamePrefix = 'dummy_'

    def __init__(self, *args, **kwargs):
        super(testSyncClient, self).__init__(*args, **kwargs)
        self.gDriveParams = {}
        self.wcApiParams = {}
        self.productParserArgs = {}

    def processConfig(self, config):
        gdrive_scopes = config.get('gdrive_scopes')
        gdrive_client_secret_file = config.get('gdrive_client_secret_file')
        gdrive_app_name = config.get('gdrive_app_name')
        gdrive_oauth_clientID = config.get('gdrive_oauth_clientID')
        gdrive_oauth_clientSecret = config.get('gdrive_oauth_clientSecret')
        gdrive_credentials_dir = config.get('gdrive_credentials_dir')
        gdrive_credentials_file = config.get('gdrive_credentials_file')
        genFID = config.get('genFID')
        genGID = config.get('genGID')
        dprcGID = config.get('dprcGID')
        dprpGID = config.get('dprpGID')
        specGID = config.get('specGID')
        usGID = config.get('usGID')
        xsGID = config.get('xsGID')

        wc_api_key = config.get(self.optionNamePrefix+'wc_api_key')
        wc_api_secret = config.get(self.optionNamePrefix+'wc_api_secret')
        wp_api_key = config.get(self.optionNamePrefix+'wp_api_key')
        wp_api_secret = config.get(self.optionNamePrefix+'wp_api_secret')
        wp_user = config.get(self.optionNamePrefix+'wp_user')
        wp_pass = config.get(self.optionNamePrefix+'wp_pass')
        wp_callback = config.get(self.optionNamePrefix+'wp_callback')


        # wp_srv_offset = config.get(self.optionNamePrefix+'wp_srv_offset', 0)
        store_url = config.get(self.optionNamePrefix+'store_url', '')

        self.gDriveParams = {
            'scopes': gdrive_scopes,
            'client_secret_file': gdrive_client_secret_file,
            'app_name': gdrive_app_name,
            'oauth_clientID': gdrive_oauth_clientID,
            'oauth_clientSecret': gdrive_oauth_clientSecret,
            'credentials_dir': gdrive_credentials_dir,
            'credentials_file': gdrive_credentials_file,
            'genFID': genFID,
            'genGID': genGID,
            'dprcGID': dprcGID,
            'dprpGID': dprpGID,
            'specGID': specGID,
            'usGID': usGID,
            'xsGID': xsGID,
        }

        self.wcApiParams = {
            'api_key':wc_api_key,
            'api_secret':wc_api_secret,
            'url':store_url,
            # 'version':'wc/v1'
        }

        self.wpApiParams = {
            'api_key':wp_api_key,
            'api_secret':wp_api_secret,
            'wp_user':wp_user,
            'wp_pass':wp_pass,
            'url':store_url,
            'callback':wp_callback
        }

        self.productParserArgs = {
            'self.importName': self.importName,
            # 'itemDepth': itemDepth,
            # 'taxoDepth': taxoDepth,
            'cols': ColData_Woo.getImportCols(),
            'defaults': ColData_Woo.getDefaults(),
        }

    def test_GDrive_Read(self):
        with SyncClient_GDrive(self.gDriveParams) as client:
            print "drive file:", client.drive_file
            print "GID", client.get_gm_modtime(self.gDriveParams['genGID'])


    def test_ProdSyncClient_WC_Read(self):
        with ProdSyncClient_WC(self.wcApiParams) as client:
            # print client.service.get('products').text
            for page in client.getIterator('products'):
                if 'products' in page:
                    for page_product in page.get('products'):
                        print "PRODUCT: ", page_product

    # def test_

    def test_UsrSyncClient_WP_Read(self):
        with UsrSyncClient_WP(self.wpApiParams) as client:
            print client.service.get('users').text
            for page in client.getIterator('users'):
                if 'users' in page:
                    for page_product in page.get('users'):
                        print "USER: ", page_product




if __name__ == '__main__':
    # main()
    testSuite = unittest.TestSuite()
    testSuite.addTest(testSyncClient('test_UsrSyncClient_WP_Read'))
    testSuite.addTest(testSyncClient('test_ProdSyncClient_WC_Read'))
    unittest.TextTestRunner().run(testSuite)