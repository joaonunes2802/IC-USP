class Slice:
    slice_dict = {}
    
    def __init__(self, name, lMax, pMax, bwpMax):
        #initialize a new general slice object 
        self.name = name
        self.lMax = lMax
        self.pMax = pMax
        self.bwpMax = bwpMax
        
    @property
    def sliceDi(self):
        return self.slice_dict
    
    @slice.setter
    def slice(self):
        self.slice_dict.update({self.name: [self.lMax, self.pMax, self.bwpMax]})

    @slice.deleter
    def name(self):
        self.slice_dict.pop(self.name)

class Slices(Slice):
    def __init__(self, name, lMax, pMax, bwpMax, ton, tin, offset, bwp_):
        #inherit from parent class
        super().__init__(name, lMax, pMax, bwpMax)
        
        #Particular atributes of each slice instance
        self.ton = ton
        self.tin = tin
        self.offset = offset
        self.bwp_ = bwp_
        
    @property
    def slicesDI(self):
        return self.slice_dict
    
    @slice.setter
    def slices(self):
        self.slice_dict.update({self.name: [self.lMax, self.pMax, self.bwpMax, self.ton, self.tin, self.offset, self.bwp_]})
    
    @slice.deleter
    def names(self):
        self.slice_dict.pop(self.name)