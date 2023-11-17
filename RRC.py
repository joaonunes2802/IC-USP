"""
This file is responsible for implementation of NR RRC in context of 5G Network using
Markov Chains to model RRC states, which are, idle, connected and inactive states.
"""
import random as rd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time


def is_full(list_connected):
    if len(list_connected) < 273:
        return False

    return True

def is_inactive_full(list_inactive):
    if len(list_inactive) < 500:
        return False
    return True 


def is_idle_full(list_idle):
    if len(list_idle) == 800:
        return True

    return False


def sorteio_state(list_state):
    state = rd.randint(0, 2)
    if state == 0:
        UE = sorteio_idle(list_state[state])
    elif state == 1:
        if len(list_state[state]) > 8:
            UE = sorteio_connected(list_state[state])
        else:
            UE = sorteio_idle(list_state[0])
            state = 0
    elif state == 2:
        if len(list_state[state]) > 8:
            UE = sorteio_inactive(list_state[state])
        else:
            UE = sorteio_idle(list_state[0])
            state = 0

    return UE, state


def sorteio_idle(list_idle):
    # Sorteia um UE aleatoriamente que se encontra em uma posição entre 1 e 550
    # O limite de UE em idle é 550

    index = rd.randint(0, len(list_idle) - 1)
    UE = list_idle.pop(index)
    return UE


def sorteio_connected(list_connected):
    # Sorteia um UE aleatoriamente que se encontra em uma posição entre 1 e o tamanho atual da lista de UE connected
    # O limite de UE connected é 273

    index = rd.randint(0, len(list_connected) - 1)
    UE = list_connected.pop(index)
    return UE


def sorteio_inactive(list_inactive):
    # Sorteia aleatoriamente um UE que está em inactive
    # O limite de UE em inactive é 279

    index = rd.randint(0, len(list_inactive) - 1)
    UE = list_inactive.pop(index)
    return UE


def idle_to_connected(UE_idle, list_connected):
     # establish the connection between UE of origin and the network
    list_connected.append(UE_idle)


def connected_to_inactive(UE_connected, list_inactive):
     # Put the respective UE in inactive state
    list_inactive.append(UE_connected)


def inactive_to_connected(UE_inactive, list_connected):
    # Re-establish the connection between UE of origin and the network
    list_connected.append(UE_inactive)


def inactive_to_idle(UE_inactive, list_idle):
    # Releasement of UE resources
    list_idle.append(UE_inactive)


def connected_to_idle(UE_connected, list_idle):
    # Releasement of UE resources
    list_idle.append(UE_connected)


def transition(UE, list_idle, list_connected, list_inactive, state):
    if UE == 0:
        '''
        p = [idle-> idle, idle-> connected], [connected->idle, connected-> inactive], [inactive-> idle, inactive-> connected]
        '''
        p1 = [0.1, 0.9]
        p2 = [0.3, 0.7]
        p3 = [0.4, 0.6]
        if state == 0:  # UE em idle
            time.sleep(0.0001)
            next = np.random.choice([0, 1], p=p1)  # Escolhe aleatoriamente se ficará em idle ou irá para connected, com base na probabilidade p1
            if next == 1 and is_full(list_connected) is False:
                idle_to_connected(UE, list_connected)
            elif next == 0 and is_idle_full(list_idle) is False:
                list_idle.append(UE)
        elif state == 1:  # UE em connected
            time.sleep(0.001)
            next = np.random.choice([0, 1], p=p2)  # Escolhe aleatoriamente se retorna para idle, ou vai para inactive, com base na probabilidade p2
            if next == 0 and is_idle_full(list_idle) is False:  
                connected_to_idle(UE, list_idle)
            elif next == 0 and is_idle_full(list_idle) is True:
                if is_inactive_full(list_inactive) is False:
                    connected_to_inactive(UE, list_inactive)
            elif next == 1 and is_inactive_full(list_inactive) is False:
                connected_to_inactive(UE, list_inactive)
            elif next == 1 and is_inactive_full(list_inactive) is True:
                if is_idle_full(list_idle) is False:
                    connected_to_idle(UE, list_idle)
        elif state == 2:  # UE em inactive
            time.sleep(0.008)
            next = np.random.choice([0, 1], p=p3)  # Escolhe alçeatoriamente se retorna para idle, ou para connected, com base na probabilidade p3
            if next == 1 and is_full(list_connected) is False:
                inactive_to_connected(UE, list_connected)
            elif next == 1 and is_full(list_connected) is True:
                if is_idle_full(list_idle) is False:
                    inactive_to_idle(UE, list_idle)
            elif next == 0 and is_idle_full(list_idle) is False:
                inactive_to_idle(UE, list_idle)
            elif next == 0 and is_idle_full(list_idle) is True:
                if is_inactive_full(list_inactive) is False:
                    list_inactive.append(UE)
    else:
        '''
        p = [idle-> idle, idle-> connected], [connected->idle, connected-> inactive], [inactive-> idle, inactive-> connected]
        '''
        p1= [0.01, 0.99]
        p2 = [0.1, 0.9]
        p3 = [0.2, 0.8]
        if state == 0:  # UE em idle
            time.sleep(0.0001)
            next = np.random.choice([0, 1], p=p1)  # Escolhe aleatoriamente se ficará em idle ou irá para connected, com base na probabilidade p1
            if next == 1 and is_full(list_connected) is False:
                idle_to_connected(UE, list_connected)
            elif next == 0 and is_idle_full(list_idle) is False:
                list_idle.append(UE)
        elif state == 1:  # UE em connected
            time.sleep(0.008)
            next = np.random.choice([0, 1], p=p2)  # Escolhe aleatoriamente se retorna para idle, ou vai para inactive, com base na probabilidade p2
            if next == 0 and is_idle_full(list_idle) is False:  
                connected_to_idle(UE, list_idle)
            elif next == 0 and is_idle_full(list_idle) is True:
                if is_inactive_full(list_inactive) is False:
                    connected_to_inactive(UE, list_inactive)
            elif next == 1 and is_inactive_full(list_inactive) is False:
                connected_to_inactive(UE, list_inactive)
            elif next == 1 and is_inactive_full(list_inactive) is True:
                if is_idle_full(list_idle) is False:
                    connected_to_idle(UE, list_idle)
        elif state == 2:  # UE em inactive
            time.sleep(0.001)
            next = np.random.choice([0, 1], p=p3)  # Escolhe alçeatoriamente se retorna para idle, ou para connected, com base na probabilidade p3
            if next == 1 and is_full(list_connected) is False:
                inactive_to_connected(UE, list_connected)
            elif next == 1 and is_full(list_connected) is True:
                if is_idle_full(list_idle) is False:
                    inactive_to_idle(UE, list_idle)
            elif next == 0 and is_idle_full(list_idle) is False:
                inactive_to_idle(UE, list_idle)
            elif next == 0 and is_idle_full(list_idle) is True:
                if is_inactive_full(list_inactive) is False:
                    list_inactive.append(UE)


def start():
        
    UEs_idle = []
    UEs_connected = []
    UEs_inactive = []
    states = [UEs_idle, UEs_connected, UEs_inactive]
    y = []
    z = []
    w = []
    x = []


    time_end = time.time() + 30


    while time.time() < time_end:
        if is_idle_full(UEs_idle) is False:
            UEs_idle.append(rd.randint(0, 1))  # Entrada de usuários na rede, 0 -> baixo consumo, 1 -> alto consumo
        
        UE, state = sorteio_state(states)
        transition(UE, UEs_idle, UEs_connected, UEs_inactive, state)
        y.append(len(UEs_idle))
        z.append(len(UEs_connected))
        w.append((len(UEs_inactive)))
        x.append(datetime.datetime.now())

    print(UEs_idle)
    print(f"Quantidade de UE idle: {len(UEs_idle)}", end='\n\n')
    print(UEs_connected)
    print(f"Quantidade de UE connected: {len(UEs_connected)}", end='\n\n')
    print(UEs_inactive)
    print(f"Quantidade de UE inactive: {len(UEs_inactive)}", end='\n\n')

    plt.plot(x, y, "-b", label="UE_Idle")
    plt.plot(x, z, "-r", label="UE_Connected")
    plt.plot(x, w, "-g", label="UE_Inactive")
    plt.legend(loc="upper left")
    plt.show()


start()
