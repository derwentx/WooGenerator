from collections import OrderedDict
from utils import listUtils

class ColData_Base(object):

    def __init__(self, data):
        super(ColData_Base, self).__init__()
        assert issubclass(type(data), dict), "Data should be a dictionary subclass"
        self.data = data
        
    def getImportCols(self):
        imports = []
        for col, data in self.data.items():
            if data.get('import', False):
                imports.append(col)
        return imports

    def getDefaults(self):
        defaults = {}
        for col, data in self.data.items():
            # if data.get('import') and data.get('default'):
            if data.get('default'):
                    defaults[col] = data.get('default')
        return defaults

    def getExportCols(self, schema=None):
        if not schema: return None
        exportCols = OrderedDict()
        for col, data in self.data.items():
            if data.get(schema, ''):
                exportCols[col] = data
        return exportCols

    def getColNames(self, cols):
        colNames = OrderedDict()
        for col, data in cols.items():
            label = data.get('label','')
            colNames[col] = label if label else col
        return colNames

class ColData_MYO(ColData_Base):

    data = OrderedDict([
        ('codesum', {
            'label': 'Item Number',
            'product':True,
        }),
        ('itemsum', {
            'label': 'Item Name',
            'product':True,
        }),
        ('WNR', {
            'label': 'Selling Price',
            'import': True,
            'product': True,
            'pricing': True,
        }),
        ('RNR',{
            'label': 'Price Level B, Qty Break 1',
            'import': True,
            'product': True,
            'pricing': True,
        }),
        ('DNR',{
            'label': 'Price Level C, Qty Break 1',
            'import': True,
            'product': True,
            'pricing': True,
        }),
        ('CVC', {
            'label': 'Custom Field 1',
            'product': True,
            'import': True,
            'default': 0
        }),
        ('descsum', {
            'label': 'Description',
            'product': True,
        }),
        ('HTML Description',{
            'import': True,
        }),
        ('Sell', {
            'default':'S',
            'product':True,
        }),
        ('Tax Code When Sold', {
            'default':'GST',
            'product': True,
        }),
        ('Sell Price Inclusive', {
            'default':'X',
            'product':True,
        }),
        ('Income Acct', {
            'default':'41000',
            'product':True,
        }),
        ('Inactive Item', {
            'default':'N',
            'product':True,
        }),
        ('use_desc', {
            'label':'Use Desc. On Sale',
            'default':'X',
            'product':True
        })
    ])

    def __init__(self, data=None):
        if not data: data = self.data
        super(ColData_MYO, self).__init__(data)

    def getProductCols(self):
        return self.getExportCols('product')

class ColData_Woo(ColData_Base):

    data = OrderedDict([
        ('parent_SKU',{
            'variation':True,
        }),
        ('codesum',{
            'label':'SKU',
            'tag':'SKU',
            'product': True,
            'variation': True,
            'category': True,
        }),
        ('itemsum', {
            'tag':'Title',
            'label':'post_title',
            'product':True, 
            'variation': True
        }),
        ('title_1', {
            'label': 'meta:title_1',
            'product':True
        }),
        ('title_2', {
            'label': 'meta:title_2',
            'product':True
        }),
        ('taxosum',{
            'label':'category_title',
            'category':True,
        }),
        ('prod_type', {
            'label':'tax:product_type',
            'product':True,
        }),
        ('catsum',{
            'label':'tax:product_cat',
            'product':True,
        }),
        ('descsum', {
            'label':'post_content',
            'tag':'Description',
            'product': True,
            'category': True,
        }),
        ('imgsum',{
            'label':'Images',
            'product': True,
            'variation': True,
            'category': True,
        }),
        ('rowcount', {
            'label':'menu_order',
            'product': True,
            'category': True,
            'variation': True
        }),
        ('PA', {
            'import': True
        }),
        ('VA', {
            'import': True
        }),
        ('D', {
            'label': 'meta:wootan_danger',
            'import': True,
            'product': True,
            'variation': True,
            'shipping': True,
        }),
        ('E',{
            'import': True,
        }),
        ('DYNCAT', {
            'import':True,
            'category': True,
            'product':True,
            'pricing': True,
        }),
        ('DYNPROD', {
            'import':True,
            'category': True,
            'product':True,
            'pricing': True,
        }),
        ('VISIBILITY', {
            'import':True,
        }),
        ('catalog_visibility', {
            'product':True,
            'default':'visible'    
        }),
        ('SCHEDULE', {
            'import':True,
            'category':True,
            'product':True,
            'pricing': True,
            'default':''
        }),
        ('spsum', {
            'tag': 'active_specials',
            'product':True,
            'variation':True,
            'pricing':True,
        }),
        ('dprclist', {
            'label': 'meta:dynamic_category_rulesets',
            # 'pricing': True,
            # 'product': True,
            # 'category': True  
        }),
        ('dprplist', {
            'label': 'meta:dynamic_product_rulesets',
            # 'pricing': True,
            # 'product': True,
            # 'category': True
        }),
        ('dprcIDlist', {
            'label': 'meta:dynamic_category_ruleset_IDs',
            'pricing': True,
            'product': True,
            # 'category': True  
        }),
        ('dprpIDlist', {
            'label': 'meta:dynamic_product_ruleset_IDs',
            'product': True,
            'pricing': True,
            # 'category': True
        }),
        ('dprcsum', {
            'label': 'meta:DPRC_Table',
            'product': True,   
            'pricing': True,
        }),
        ('dprpsum', {
            'label': 'meta:DPRP_Table',
            'product': True,   
            'pricing': True,
        }),
        ('price', {
            'label':'regular_price',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('sale_price', {
            'label':'sale_price',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('sale_price_dates_from', {
            'label':'sale_price_dates_from',
            'tag':'sale_from',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('sale_price_dates_to', {
            'label':'sale_price_dates_to',
            'tag':'sale_to',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('RNR', {
            'label': 'meta:lc_rn_regular_price',
            'import': True,
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('RNS', {
            'label': 'meta:lc_rn_sale_price',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('RNF', {
            'label': 'meta:lc_rn_sale_price_dates_from',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('RNT', {
            'label': 'meta:lc_rn_sale_price_dates_to',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('RPR', {
            'label': 'meta:lc_rp_regular_price',
            'import': True,
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('RPS', {
            'label': 'meta:lc_rp_sale_price',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('RPF', {
            'label': 'meta:lc_rp_sale_price_dates_from',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('RPT', {
            'label': 'meta:lc_rp_sale_price_dates_to',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('WNR', {
            'label': 'meta:lc_wn_regular_price',
            'import': True,
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('WNS', {
            'label': 'meta:lc_wn_sale_price',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('WNF', {
            'label': 'meta:lc_wn_sale_price_dates_from',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('WNT', {
            'label': 'meta:lc_wn_sale_price_dates_to',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('WPR', {
            'label': 'meta:lc_wp_regular_price',
            'import': True,
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('WPS', {
            'label': 'meta:lc_wp_sale_price',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('WPF', {
            'label': 'meta:lc_wp_sale_price_dates_from',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('WPT', {
            'label': 'meta:lc_wp_sale_price_dates_to',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('DNR', {
            'label': 'meta:lc_dn_regular_price',
            'import': True,
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('DNS', {
            'label': 'meta:lc_dn_sale_price',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('DNF', {
            'label': 'meta:lc_dn_sale_price_dates_from',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('DNT', {
            'label': 'meta:lc_dn_sale_price_dates_to',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('DPR', {
            'label': 'meta:lc_dp_regular_price',
            'import': True,
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('DPS', {
            'label': 'meta:lc_dp_sale_price',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('DPF', {
            'label': 'meta:lc_dp_sale_price_dates_from',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('DPT', {
            'label': 'meta:lc_dp_sale_price_dates_to',
            'product': True,
            'variation': True,
            'pricing': True,
        }),
        ('CVC', {
            'label': 'meta:commissionable_value',
            'import': True,
            'product': True,
            'variation': True,
            'pricing': True,
            'default': 0
        }),
        ('weight', {
            'import': True,
            'product': True,
            'variation': True,
            'shipping': True,
        }),
        ('length', {
            'import': True,
            'product': True,
            'variation': True,
            'shipping':True
        }),
        ('width', {
            'import': True,
            'product': True,
            'variation': True,
            'shipping': True,
        }),
        ('height', {
            'import': True,
            'product': True,
            'variation': True,
            'shipping': True,
        }),
        ('stock', {
            'import': True,
            'product': True,
            'variation': True,
            'inventory':True
        }),
        ('stock_status', {
            'import': True,
            'product': True,
            'variation': True,
            'inventory':True
        }),
        ('manage_stock', {
            'product': True,
            'variation': True,
            'inventory':True
        }),
        ('Images',{
            'import': True,
            'default': ''
        }),
        ('HTML Description', {
            'import': True,
        }),
        ('last_import',{
            'label':'meta:last_import',
            'product': True,
        })
    ])

    def __init__( self, data = None):
        if not data: data = self.data
        super(ColData_Woo, self).__init__( data )

    def getProductCols(self):
        return self.getExportCols('product')

    def getVariationCols(self):
        return self.getExportCols('variation')

    def getCategoryCols(self):
        return self.getExportCols('category')

    def getPricingCols(self):
        return self.getExportCols('pricing')

    def getShippingCols(self):
        return self.getExportCols('shipping')

    def getInventoryCols(self):
        return self.getExportCols('inventory')

    def getAttributeCols(self, attributes, vattributes):
        attributeCols = OrderedDict()
        all_attrs = listUtils.combineLists(attributes.keys(), vattributes.keys())
        for attr in all_attrs:
            attributeCols['attribute:'+attr] = {
                'product':True,
            }
            if attr in vattributes.keys():
                attributeCols['attribute_default:'+attr] = {
                    'product':True,
                }
                attributeCols['attribute_data:'+attr] = {
                    'product':True,
                }
        return attributeCols

    def getAttributeMetaCols(self, vattributes):
        atttributeMetaCols = OrderedDict()
        for attr in vattributes.keys():
            atttributeMetaCols['meta:attribute_'+attr] = {
                'variable': True,
                'tag': attr
            }
        return atttributeMetaCols

class ColData_User(ColData_Base):

    data = OrderedDict([
        ('Wordpress Username',{
            'label':'Username',
            'user':True,
            'report': True,
            'import':True,
            'sync':'slave_override',
            'warn':True,
        }),
        ('MYOB Card ID',{
            'label':'myob_card_id',
            'import':True,
            'user':True,
            'report':True,
            'sync':'master_override',
            'warn':True,
        }),
        ('MYOB Customer Card ID',{
            'label':'myob_customer_card_id',
            'import':True,
            # 'report':True,
            'user':True,
            'sync':'master_override',
            'warn':True,
        }),
        ('Client Grade',{
            'import':True,
            'label':'client_grade',
            'user':True,
            'report':True,
            'sync':'master_override',
            'warn':True,
        }),
        ('Direct Brand', {
            'import':True,
            'label':'direct_brand',
            'user':True,
            'report': True,
            'sync':'master_override',
            'warn':True,
        }),
        ('Agent', {
            'label':'agent',
            'import':'true',
            'user':True,
            'sync':'master_override',
            'warn':True,
        }),
        ('E-mail', {
            'label':'user_email',
            'import': True,
            'user':True,
            'report': True,
            'sync':True,
            'warn':True,
            'static':True,
        }),
        ('Role', {
            'label': 'act_role',
            'import':True,
            'user':True,
            'report': True,
            'sync':True,
            'warn': True,
            'static':True,
        }),
        ('First Name', {
            'label':'first_name',
            'import':True,
            'user':True,
            'report': True,
            'sync':True,
            'warn': True,
            'static':True,
        }),
        ('Surname', {
            'label':'last_name',
            'import': True,
            'user':True,
            'report': True,
            'sync':True,
            'warn': True,
            'static':True,
        }),
        ('Company',{
            'label':'billing_company',
            'import':True,
            'user':True,
            'report': True,
            'sync':True,
            'warn': True,
            'static':True,
        }),
        ('Mobile Phone',{
            'label':'mobile_number',
            'import':True,
            'user':True,
            'sync':True,
            'report':True,
            'warn': True,
            'static':True,
        }),
        ('Phone',{
            'label':'billing_phone',
            'import':True,
            'user':True,
            'report': True,
            'sync':True,
            'warn': True,
            'static':True,
        }),
        ('Contact',{
            'import':True,
            'label':'nickname',
            'user':True,
            'sync':True,
        }),
        ('Birth Date',{
            'label':'birth_date',
            'import':True,
            'user':True,
            'sync':True,
        }),
        ('Fax',{
            'label':'fax_number',
            'import':True,
            'user':True,
            'sync':True,
        }),
        ('Address 1',{
            'label':'billing_address_1',
            'import':True,
            'user':True,
            'sync':True,
            'warn': True,
            'static':True,
        }),
        ('Address 2',{
            'label':'billing_address_2',
            'import':True,
            'user':True,
            'sync':True,
            'warn': True,
            'static':True,
        }),
        ('City',{
            'label':'billing_city',
            'import':True,
            'user':True,
            'sync':True,
            'warn': True,
            'static':True,
            'report': True,
        }),
        ('Postcode',{
            'label':'billing_postcode',
            'import':True,
            'user':True,
            'sync':True,
            'warn': True,
            'static':True,
            'report': True,
        }),
        ('State',{
            'label':'billing_state',
            'import':True,
            'user':True,
            'sync':True,
            'warn': True,
            'static':True,
            'report':True
        }),
        ('Home Address 1',{
            'label':'shipping_address_1',
            'import':True,
            'user':True,
            'sync':True,
            'static':True,
        }),
        ('Home Address 2',{
            'label':'shipping_address_2',
            'import':True,
            'user':True,
            'sync':True,
            'static':True,
        }),
        ('Home City',{
            'label':'shipping_city',
            'import':True,
            'user':True,
            'sync':True,
            'static':True,
        }),
        ('Home Postcode',{
            'label':'shipping_postcode',
            'import':True,
            'user':True,
            'sync':True,
            'static':True,
        }),
        ('Home Country',{
            'label':'shipping_country',
            'import':True,
            'user':True,
            'sync':True,
            'static':True,
        }),
        ('Home State',{
            'label':'shipping_state',
            'import':True,
            'user':True,
            'sync':True,
            'static':True,
        }),
        ('Web Site',{
            'label':'url',
            'import':True,
            'user':True,
            'sync':True,
        }),
        ('ABN',{
            'label':'abn',
            'import':True,
            'user':True,   
            'sync':True,   
            'warn': True,      
        }),
        ('Business Type',{
            'label':'business_type',
            'import':True,
            'user':True,    
            'sync':True,
        }),
        ('Lead Source',{
            'label':'how_hear_about',
            'import':True,
            'user':True,    
            'sync':True,
        }),
        ('Referred By',{
            'label':'referred_by',
            'import':True,
            'user':True,
            'sync':True,
        }),
        ('Mobile Phone Preferred',{
            'label':'pref_mob',
            'import':True,
            'user':True,
            'sync':True,
        }),
        ('Phone Preferred',{
            'label':'pref_tel',
            'import':True,
            'user':True,
            'sync':True,
        }),
        ('Personal E-mail', {
            'label':'personal_email',
            'import':True,
            'user':True,
            'report':True,
        }),
        # ('rowcount', {
        #     # 'import':True,
        #     # 'user':True,
        #     'report':True,
        # }),
        # ('Edit Date', {
        #     'import': True,
        #     'report': True
        # }),
        ('Edited in Act', {
            'import': True,
            'report': True
        }),
        ('updated', {
            'import':True,
            'report':True
        }),
    ])

    def __init__(self, data=None):
        if not data: data = self.data
        super(ColData_User, self).__init__(data)

    def getUserCols(self):
        return self.getExportCols('user')

    def getReportCols(self):
        return self.getExportCols('report')

    def getSyncCols(self):
        return self.getExportCols('sync')

if __name__ == '__main__':
    print "Testing ColData_MYO Class:"
    colData = ColData_MYO()
    print colData.getImportCols()
    print colData.getDefaults()
    print colData.getProductCols()

    print ""
    print "Testing ColData_Woo class:"
    colData = ColData_Woo()
    print colData.getImportCols()
    print colData.getDefaults()
    print colData.getProductCols()

    print ""
    print "Testing ColData_User class:"
    colData = ColData_User()
    print colData.getImportCols()

    