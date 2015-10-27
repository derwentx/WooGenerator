from collections import OrderedDict
from utils import descriptorUtils, sanitationUtils, listUtils
from csvparse_tree import CSVParse_Tree, ImportTreeItem, ImportTreeTaxo, ImportTreeObject

DEBUG_GEN = True

class ImportGenObject(ImportTreeObject):

    _isProduct = False
    codeKey = 'code'
    nameKey = 'name'
    fullnameKey = 'fullname'
    descriptionKey = 'HTML Description'
    codesumKey = 'codesum'
    descsumKey = 'descsum'
    namesumKey = 'itemsum'
    fullnamesumKey = 'fullnamesum'

    def __init__(self, *args, **kwargs):
        subs = kwargs['subs']
        regex = kwargs['regex']
        self.subs = subs
        self.regex = regex
        super(ImportGenObject, self).__init__(*args, **kwargs)

    @classmethod
    def fromImportTreeObject(cls, objectData, regex, subs):
        assert isinstance(objectData, ImportTreeObject)
        row = objectData.row
        rowcount = objectData.rowcount
        depth = objectData.getDepth()
        meta = objectData.getMeta()
        parent = objectData.getParent()
        return cls(objectData, rowcount, row, depth, meta, parent, regex, subs)

    @property
    def isProduct(self): return self._isProduct

    def verifyMeta(self):
        keys = [
            self.codeKey,
            self.nameKey,
            self.fullnameKey,
            self.namesumKey,
            self.codesumKey,
            self.descsumKey,
            self.fullnamesumKey
        ]
        for key in keys:
            assert key in self.keys()
            # if key in self.keys():
            #     self.registerMessage("{} is set".format( key ) )
            # else:
            #     self.registerError("{} is not set".format( key ), "verifyMeta")

    code        = descriptorUtils.safeKeyProperty(codeKey)
    name        = descriptorUtils.safeKeyProperty(nameKey)
    fullname    = descriptorUtils.safeKeyProperty(fullnameKey)
    namesum     = descriptorUtils.safeKeyProperty(namesumKey)
    description = descriptorUtils.safeKeyProperty(descriptionKey)
    codesum     = descriptorUtils.safeKeyProperty(codesumKey)
    descsum     = descriptorUtils.safeKeyProperty(descsumKey)
    fullnamesum = descriptorUtils.safeKeyProperty(fullnamesumKey)

    @property
    def index(self):
        return self.codesum

    def getNameAncestors(self):
        return self.getAncestors()

    def getCodeDelimeter(self, other):
        return ''

    def joinCodes(self):
        ancestors = [ancestor for ancestor in self.getAncestors() + [self] if ancestor.code ]
        if not ancestors: 
            return ""
        prev = ancestors.pop(0)
        codesum = prev.code
        while ancestors:
            this = ancestors.pop(0)
            codesum += this.getCodeDelimeter(prev) + this.code
            prev = this
        return codesum

    def joinDescs(self):
        if self.description: 
            return self.description
        fullnames = [self.fullname]
        ancestors = self.getAncestors()
        for ancestor in reversed(ancestors):
            ancestorDescription = ancestor.description
            if ancestorDescription:
                return ancestorDescription
            ancestorFullname = ancestor.fullname
            if ancestorFullname: 
                fullnames.insert(0, ancestorFullname)
        if fullnames:
            return " - ".join(reversed(fullnames))
        else:
            return ""

    def getNameDelimeter(self):
        return ' '

    def joinNames(self):
        ancestors = self.getNameAncestors() + [self]
        names = listUtils.filterUniqueTrue(map(lambda x: x.name, ancestors))
        nameDelimeter = self.getNameDelimeter()
        return nameDelimeter.join ( names )     

    def joinFullnames(self):
        ancestors = self.getNameAncestors() + [self]
        names = listUtils.filterUniqueTrue(map(lambda x: x.fullname, ancestors))
        nameDelimeter = self.getNameDelimeter()
        return nameDelimeter.join ( names )      

    def changeName(self, name):
        return sanitationUtils.shorten(self.regex, self.subs, name)

    def processMeta(self):

        meta = self.getMeta()
        try:
            self.fullname =  meta[0] 
        except:
            self.fullname =  "" 
        self.registerMessage("fullname: {}".format(self.fullname ) )

        try:
            self.code = meta[1] 
        except:
            self.code = "" 
        self.registerMessage("code: {}".format(self.code ) )

        codesum = self.joinCodes()
        self.registerMessage("codesum: {}".format(codesum) )
        self.codesum = codesum

        descsum = self.joinDescs()
        self.registerMessage("descsum: {}".format( descsum ) )
        self.descsum = descsum   

        name = self.changeName(self.fullname)
        self.registerMessage("name: {}".format(name ) )
        self.name = name

        namesum = self.joinNames()
        self.registerMessage("namesum: {}".format(namesum) )
        self.namesum = namesum  

        fullnamesum = self.joinFullnames()
        self.registerMessage("fullnamesum: {}".format(fullnamesum) )
        self.fullnamesum = fullnamesum  


class ImportGenItem(ImportGenObject, ImportTreeItem):

    # def __init__(self, *args, **kwargs):
    #     super(ImportGenItem, self).__init__(*args, **kwargs)

    def getNameAncestors(self):
        return self.getItemAncestors()

    def getCodeDelimeter(self, other):
        assert isinstance(other, ImportGenObject)
        if not other.isRoot and other.isTaxo:
            return '-'
        else:
            return super(ImportGenItem, self).getCodeDelimeter(other)

class ImportGenProduct(ImportGenItem):

    _isProduct = True

class ImportGenTaxo(ImportGenObject, ImportTreeTaxo):

    namesumKey = 'taxosum'
    namesum     = descriptorUtils.safeKeyProperty(namesumKey)

    # def __init__(self, *args, **kwargs):
    #     super(ImportGenTaxo, self).__init__(*args, **kwargs)

    def getNameDelimeter(self):
        return ' > '

class CSVParse_Gen(CSVParse_Tree):

    taxoContainer = ImportGenTaxo
    itemContainer = ImportGenItem
    productContainer = ImportGenProduct

    def __init__(self, cols, defaults, schema, \
                    taxoSubs={}, itemSubs={}, taxoDepth=2, itemDepth=2, metaWidth=2):
        assert metaWidth >= 2, "metaWidth must be greater than 2 for a GEN subclass"
        extra_defaults = OrderedDict([
            ('CVC', '0'),   
            ('code', ''),
            ('name', ''),
            ('fullname', ''),   
            ('description', ''),
            ('HTML Description', ''),
            ('imglist', [])
        ])
        extra_taxoSubs = OrderedDict([
            ('', ''),
        ])
        extra_itemSubs = OrderedDict([
            ('Hot Pink', 'Pink'),
            ('Hot Lips (Red)', 'Red'),
            ('Hot Lips', 'Red'),
            ('Silken Chocolate (Bronze)', 'Bronze'),
            ('Silken Chocolate', 'Bronze'),
            ('Moon Marvel (Silver)', 'Silver'),
            ('Dusty Gold', 'Gold'),
            
            ('Screen Printed', ''),
            ('Embroidered', ''),
        ])
        extra_cols = [schema]

        cols = listUtils.combineLists( cols, extra_cols )
        defaults = listUtils.combineOrderedDicts( defaults, extra_defaults )
        super(CSVParse_Gen, self).__init__( cols, defaults, taxoDepth, itemDepth, metaWidth)

        self.schema     = schema
        self.taxoSubs   = listUtils.combineOrderedDicts( taxoSubs, extra_taxoSubs )
        self.itemSubs   = listUtils.combineOrderedDicts( itemSubs, extra_itemSubs )   
        self.taxoRegex  = sanitationUtils.compileRegex(self.taxoSubs)
        self.itemRegex  = sanitationUtils.compileRegex(self.itemSubs)
        self.productIndexer = self.getGenCodesum
        # if DEBUG_GEN:
        #     print "GEN initializing: "
        #     print "-> taxoDepth: ", self.taxoDepth
        #     print "-> itemDepth: ", self.itemDepth
        #     print "-> maxDepth: ", self.maxDepth
        #     print "-> metaWidth: ", self.metaWidth


    def clearTransients(self):
        super(CSVParse_Gen, self).clearTransients()
        self.products   = OrderedDict() 

    def registerProduct(self, prodData):
        assert prodData.isProduct
        self.registerAnything(
            prodData, 
            self.products,
            indexer = self.productIndexer,
            singular = True,
            resolver = self.resolveConflict,
            registerName = 'products'
        )

    def registerItem(self, itemData):
        super(CSVParse_Gen, self).registerItem(itemData)
        if itemData.isProduct:
            self.registerProduct(itemData)

    def changeItem(self, item):
        return sanitationUtils.shorten(self.itemRegex, self.itemSubs, item)

    def changeFullname(self, item):
        subs = OrderedDict([(' \xe2\x80\x94 ', ' ')])
        return sanitationUtils.shorten(sanitationUtils.compileRegex(subs), subs, item)

    def depth(self, row):
        for i, cell in enumerate(row):
            if cell: 
                return i
            if i >= self.maxDepth: 
                return -1
        return -1

    def sanitizeCell(self, cell):
        return sanitationUtils.sanitizeCell(cell)  

    def getGenCodesum(self, genData):
        assert isinstance(genData, ImportGenObject)
        return genData.codesum

    def getContainer(self, allData, **kwargs):
        container = super(CSVParse_Gen, self).getContainer( allData, **kwargs)
        if issubclass( container, ImportGenItem ):
            itemtype = allData.get(self.schema,'')
            self.registerMessage("itemtype: {}".format(itemtype))
            if itemtype in self.prod_containers.keys():
                container = self.prod_containers[itemtype]
        return container

    def getKwargs(self, allData, container, **kwargs):
        kwargs = super(CSVParse_Gen, self).getKwargs(allData, container, **kwargs)
        assert issubclass(container, ImportGenObject)
        if issubclass(container, self.taxoContainer):
            regex = self.taxoRegex
            subs = self.taxoSubs
        else:
            assert issubclass(container, self.itemContainer), "class must be item or taxo subclass not %s" % container.__name__
            regex = self.itemRegex
            subs = self.itemSubs
        kwargs['regex'] = regex
        kwargs['subs'] = subs
        for key in ['regex', 'subs']:
            assert kwargs[key] is not None
        return kwargs

    # def newObject(self, rowcount, row, **kwargs):
    #     return super(CSVParse_Gen, self).newObject(rowcount, row, **kwargs)

    def getProducts(self):
        self.registerMessage("returning products: {}".format(self.products.keys()))
        return self.products
