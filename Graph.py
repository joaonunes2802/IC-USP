from Slices import Slice, Slices
from BWPs import BWP
from CDRX import C_DRX

class Graph(): 
    
    availableBandwidth = 250  #MHz
    bwpeMBB = 130
    bwpURLLC = 100
    bwpmMTC = 20
    lMaxeMBB = 500  # 500 ms
    lMaxURLLC = 1
    lMaxmMTC = 1000
    pmaxeMBB = 20 #watts
    pmaxURLLC = 40
    pmaxmMTC = 10
    
    
    @classmethod
    def creationNode(cls, sliceType, nodeNumber, tNodes):
        if 'eMBB' in sliceType:
            i = 0
            while i <= tNodes:
                times = C_DRX()
                CDRXparameters = times.cdrxConfig(sliceType)
                ton = CDRXparameters["Ton"]
                offset = CDRXparameters["Offset"]
                cycleLength = CDRXparameters["Cycle Length"]
                tin = cycleLength - offset - ton
                lUsed = tin + offset
                
                bwps = BWP()
                bwp_ = bwps.allocate_bwp(sliceType)
                

                eMBBNode = Slices(sliceType + str(nodeNumber), cls.lMaxeMBB, cls.pmaxeMBB, cls.bwpeMBB, ton, tin, offset, bwp_, lUsed).slices
                i+=1
            return eMBBNode
        elif 'URLLC' in sliceType:
            i = 0
            while i <= tNodes:
                times = C_DRX()
                CDRXparameters = times.cdrxConfig(sliceType)
                ton = CDRXparameters["Ton"]
                offset = CDRXparameters["Offset"]
                cycleLength = CDRXparameters["Cycle Length"]
                tin = cycleLength - offset - ton
                lUsed = tin + offset
                
                bwps = BWP()
                bwp_ = bwps.allocate_bwp(sliceType)
                
                URLLCNode = Slices(sliceType + str(nodeNumber), cls.lMaxURLLC, cls.pmaxURLLC, cls.bwpURLLC, ton, tin, offset, bwp_, lUsed).slices
                i+=1
            return URLLCNode
        elif 'mMTC' in sliceType:
            i = 0
            while i <= tNodes:
                times = C_DRX()
                CDRXparameters = times.cdrxConfig(sliceType)
                ton = CDRXparameters["Ton"]
                offset = CDRXparameters["Offset"]
                cycleLength = CDRXparameters["Cycle Length"]
                tin = cycleLength - offset - ton
                lUsed = tin + offset
                
                bwps = BWP()
                bwp_ = bwps.allocate_bwp(sliceType)
                
                mMTCNode = Slices(sliceType + str(nodeNumber), cls.lMaxmMTC, cls.pmaxmMTC, cls.bwpmMTC, ton, tin, offset, bwp_, lUsed).slices
                i+=1
            return mMTCNode
        else:
            return None
    
    
    @classmethod
    def updateNode(cls, srcNode, destNode):
        L1 = srcNode.latency()
        L2 = destNode.latency()
        
        newL = L1[1] + L2[1]
        
        bwp1 = srcNode.bwp()
        bwp2 = srcNode.bwp()
        
        newBwp = bwp1[1] + bwp2[1]
        
        srcNode.slices(newL, newBwp)
        destNode.slices(newL, newBwp)