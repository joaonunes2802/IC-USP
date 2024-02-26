'''
This python program implements the algorithm proposed in section 3 of the article "On using Deep Reinforcement Learning to balance
Power Consumption and Latency in 5G NR" in which is an optimization algorithm to derive the best C-DRX parameters and Bandwitch Part 
(BWP) configuration while guaranteeing a low Power Comsuption (PC) and avoiding the latency overflow
'''

import random as rd
#import numpy as np

# K UEs
UEs = []
# UEs = [ue0, ue1]
#ue0 = [[dij], [fij], [gij], [wij]]
      
#----- C-DRX Parameters -----

W = []  # W possibles bandwidtch lenght in percentage
for i in range(0,2):
    W.append(rd.random())


delta = []  # Set of Cycle Lenghts
for i in range(0,2):
    delta.append(rd.randint(1, 3))  # Cycles lenght between 1 and 3
    

fi = []  # Set of ON periods
for d in delta:
    if d != 1:
        fi.append(rd.random())
    else:
        fi.append(d/10)  # guarantee that ON period is shorter than Cycle lenght


gama = []  # Set of offsets
for d, f in zip(delta, fi):
    if d != 1:
        gama.append(rd.random())
    else:
        number = 1
        while(number + f > d):
            number = rd.random()  # guarantee that offset period + ON period is 
                                  # shorter than cycle lenght
        gama.append(number)
    

S = [x for x in range(0,2)]  # Time Slots
rd.shuffle(S)


# Decision Variables 
dij = []
for i in range(0, 2):
    for j in range(0,2):
        dij.append(rd.randint(0, 1))
    
    d = dij.copy()
    UEs.append([d])
    dij.clear()



fij = []
for i in range(0,2):
    for j in range(0, 2):
        fij.append(rd.randint(0, 1))
    
    f = fij.copy()
    UEs[i].append(f)
    fij.clear()



gij = []
for i in range(0,2):
    for j in range(0, 2):
        gij.append(rd.randint(0, 1))
    
    g = gij.copy()
    UEs[i].append(g)
    gij.clear()

wij = []
for i in range(0,2):
    for j in range(0, 2):
        wij.append(rd.randint(0, 1))
    
    w = wij.copy()
    UEs[i].append(w)
    wij.clear()

#print(UEs)
#print(UEs[1])
#print(UEs[1][3])


# Power Comsuption
Pit = []    
Pmax = 100


# Delay variable
Lit = []
Limax = 100


#print(UEs)
#print(W)

# Beta function
def beta(UEs, W):
    beta = []
    soma = 0
    for i in range(0, len(UEs)):
        for j in range(0, len(W)):
            soma += (UEs[i][3][j] * W[j])
        
        b = 0.4 + (0.6*((soma - 20)/80))
        beta.append(b)
        #print(soma)
        #print(b)
    
    return beta

beta = beta(UEs, W)
        
#print(beta)


# Objective function
'''
def objectiveFunction(alpha, beta):
    soma1 = 0
    soma2 = []
    for ue in UEs:
        for t in S:
            soma1 += ((ue[t][0]/Limax)* alpha) + ((1 - alpha)*((ue[t][1] * beta)/Pmax))
        
        soma2.append(soma1)
    return soma2
'''
          
