class Parameters:
    
    @staticmethod
    def capacity(BWPmax, BWPused, BWPrequested):
        return BWPmax - BWPused - BWPrequested
    
    
    @staticmethod
    def ntf(connections):
        return sum(connections)
    
    
    '''@staticmethod
    def nbf(nodes, nNumber, bwpLink, bwpRequest):
        bwpCapacity = []
        for i in nodes:
            if nodes.index(i) != nNumber:
                bwpCapacity.append(bwpLink - bwpRequest)
        
        
        return bwpCapacity'''
    
    
    @staticmethod
    def nccf(lengths):
        return (sum(lengths) ** (-1))
    
    
    @staticmethod
    def nodeLatency(lMax, lUsed, lRequested):
        return lMax - lUsed - lRequested
    