class MainSlices:
    bwpB = 10  #bandwith part for eMBB
    bwpT = bwpB - 5  #bandwith part for mMTC
    bwpU = bwpB - 3  #bandwith part for URLLC
    
    @classmethod
    def allocate_bwp(cls, nameSlice):
        if 'eMBB' in nameSlice:
            return cls.bwpB
        elif 'mMTC' in nameSlice:
            return cls.bwpT
        elif 'URLLC' in nameSlice:
            return cls.bwpU
        else:
            return None
