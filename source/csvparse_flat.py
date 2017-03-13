# from csvparse_woo import ImportWooProduct
# from copy import deepcopy
# from collections import OrderedDict
# from coldata import ColData_User, ColData_Woo
# from contact_objects import ContactAddress, ContactName, ContactPhones, SocialMediaFields
from csvparse_abstract import CSVParse_Base, ImportObject, ObjList
from utils import descriptorUtils, listUtils, SanitationUtils, TimeUtils
# import os
# import time
# from pprint import pprint
# import operator
# import re

usrs_per_file = 1000

class ImportFlat(ImportObject):
    pass

class CSVParse_Flat(CSVParse_Base):
    objectContainer = ImportFlat
    # def __init__(self, cols, defaults):
    #     super(CSVParse_Flat, self).__init__(cols, defaults)

class ImportSpecial(ImportFlat):

    ID = descriptorUtils.safeKeyProperty('ID')
    start_time = descriptorUtils.safeKeyProperty('start_time')
    end_time = descriptorUtils.safeKeyProperty('end_time')

    # @property
    # def start_time_iso(self): return TimeUtils.isoTimeToString(self.start_time)

    # @property
    # def end_time_iso(self): return TimeUtils.isoTimeToString(self.end_time)

    def __init__(self, data, **kwargs):
        if self.DEBUG_MRO:
            self.registerMessage(' ')
        for key in ["FROM", "TO"]:
            if key not in data:
                raise UserWarning("Missing %s field. data: %s, kwargs: %s" % (key, data, kwargs))
        super(ImportSpecial, self).__init__(data, **kwargs)
        try:
            self.ID
        except:
            raise UserWarning('ID exist for Special to be valid')

        self['start_time'] = TimeUtils.gDriveStrpTime(self['FROM'])
        self['end_time'] = TimeUtils.gDriveStrpTime(self['TO'])

    @property
    def index(self):
        return self.ID

    def getIndex(self):
        e = DeprecationWarning("use .index instead of .getIndex()")
        self.registerError(e)
        return self.index

class CSVParse_Special(CSVParse_Flat):

    objectContainer = ImportSpecial

    def __init__(self, cols=None, defaults=None):
        if self.DEBUG_MRO:
            self.registerMessage(' ')
        if cols is None:
            cols = []
        if defaults is None:
            defaults = {}
        extra_cols = [
            "ID",
            "FROM",
            "TO",
            "RNS",
            "RPS",
            "WNS",
            "WPS",
            "XRNS",
            "XRPS",
            "XWNS",
            "XWPS"
        ]
        cols = listUtils.combineLists(cols, extra_cols)

        super(CSVParse_Special, self).__init__(cols, defaults)
        self.objectIndexer = self.getObjectID

    @classmethod
    def getObjectID(self, objectData):
        return objectData.ID

class ImportSqlProduct(ImportFlat):
    ID          = descriptorUtils.safeKeyProperty('ID')
    codesum     = descriptorUtils.safeKeyProperty('codesum')
    itemsum     = descriptorUtils.safeKeyProperty('itemsum')

    @property
    def index(self):
        return self.codesum

class CSVParse_WPSQLProd(CSVParse_Flat):

    objectContainer = ImportSqlProduct

    """docstring for CSVParse_WPSQLProd"""
    # def __init__(self, arg):
        # super(CSVParse_WPSQLProd, self).__init__()
