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

W = 150  # available bandwidtch

omega = []  # W possibles bandwidtch lenght in percentage
for i in range(0,2):
    omega.append(rd.random())


delta = []  # Set of Cycle Lenghts
for i in range(0,2):
    delta.append(i + 1)  # Cycles lenght between 1 and 3
    
rd.shuffle(delta)
    

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
#rd.shuffle(S)


# Decision Variables 
dij = []
for i in range(0, 2):
    for j in range(0,2):
        if dij.count(1) == 0:
            dij.append(rd.randint(0, 1))
        else:
            dij.append(0)
    
    #print(dij)
    d = dij.copy()
    UEs.append([d])
    dij.clear()



fij = []
for i in range(0,2):
    for j in range(0, 2):
        if fij.count(1) == 0:
            fij.append(rd.randint(0, 1))
        else:
            fij.append(0)
    
    f = fij.copy()
    UEs[i].append(f)
    fij.clear()



gij = []
for i in range(0,2):
    for j in range(0, 2):
        if gij.count(1) == 0:
            gij.append(rd.randint(0, 1))
        else:
            gij.append(0)
    
    g = gij.copy()
    UEs[i].append(g)
    gij.clear()

wij = []
for i in range(0,2):
    for j in range(0, 2):
        if wij.count(1) == 0:
            wij.append(rd.randint(0, 1))
        else:
            wij.append(0)
    
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
for i in range(0, len(UEs)):
    numero = rd.randint(0, 100)
    if numero == 0:
        Lit.append(-1)
    else:
        Lit.append(numero)
Limax = 100


#print(UEs)
#print(W)


# Beta function; equation 3
def beta(UEs, omega):
    beta = []
    soma = 0
    for ue in UEs:
        for j in range(0, len(omega)):
            soma += (ue[3][j] * omega[j])
        
        b = 0.4 + (0.6*((soma - 20)/80))
        beta.append(b)
        #print(soma)
        #print(b)
    
    return beta


       
#print(beta)


# Equation 4
def equation4(UEs):
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0
    for ue in UEs:
        sum1 = sum(ue[0])
        sum2 = sum(ue[1])
        sum3 = sum(ue[2])
        sum4 = sum(ue[3])
        lista = [sum1, sum2, sum3, sum4]
        if(sum(lista)) > 4:
            return False
    
    return True
        


# equation 5

def equation5(UEs, omega, beta2):
    sum = 0
    
    for ue in UEs:
        if ue[3] == 1:
            if beta2[UEs.index(ue)] == 1:
                sum += omega[ue]        
        
    if sum > 1:
        return False
    
    return True

#print(equation5(UEs, omega))

# Equation 6

def equation6(UEs, beta2):
    beta2 = [1, 0]
    sum = 0
    Kmax = 50
    for ue in UEs:
        if beta2[UEs.index(ue)] == 1:
            sum += beta2[UEs.index(ue)]
    
    if sum <= Kmax:
        return True
    
    return False

# Equation 7

beta2 = []
def equation7(delta, fi, gama, S, UEs, omega, beta2, Pit):
    limiteSup = len(S)
    N = []
    for n in range(0, limiteSup):
        N.append(n)
    
    
    for ue, t, k in zip(UEs, S, N):
        sum1 = 0
        sum2 = 0
        sum3 = 0
        
        aux1 = 0
        for j in range(0, len(delta)):
            sum1 += (ue[0][j] * delta[j])
            
        for i in range(0, len(fi)):
            sum2 += (ue[1][i] * fi[i])
        
        for k in range(0, len(gama)):
            sum3 += (ue[2][k] * gama[k])
        
        aux1 = k * sum1
        
        if ((aux1 + sum2) <= t) and ((aux1 + sum2 + sum3) >= t):
            Pit.append(1)
            aux2 = 0
            for jj in range(0, len(omega)):
                if (ue[2][jj]) != 1:
                    aux2 = 1
            
            if aux2 == 0:
                beta2.append(1)
            else:
                beta2.append(0)
        else:
            Pit.append(0)
            beta2.append(0)

#equation7(delta, fi, gama, S, UEs, omega, beta2, Pit)
#print(beta2)
#print(Pit)
# Objective function



def objectiveFunction(alpha, beta, Pit, Pmax, Lit, Limax, S, UEs):
    sum = []
    for i in range(0, len(UEs)):
        sum1 = 0
        sum2 = 0
        for j in range(0, len(S)):
            aux1 = alpha * (Lit[i]/ Limax)
            aux2 = (1 - alpha) * ((beta[i] * Pit[i])/ Pmax)
            sum1 += (aux1 + aux2)
        
        sum2 += sum1
        sum.append(sum2)
    
    print(sum)
    return min(sum)


beta = beta(UEs, omega)  
equation7(delta, fi, gama, S, UEs, omega, beta2, Pit)

if (equation4(UEs) and equation5(UEs, omega, beta2) and equation6(UEs, beta2)) is True:
        print(objectiveFunction(0.5, beta, Pit, Pmax, Lit, Limax, S, UEs))
