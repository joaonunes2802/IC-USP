"""
This file is responsible for implementation of NR RRC in context of 5G Network using
Markov Chains to model RRC states, which are, idle, connected and inactive states.
"""
import random as rd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from time import sleep


"""
def area(width):
    points = []
    for i in range(width + 1):
        coluna = []
        for j in range(width + 1):
            coluna.append(j)
        points.append(coluna)
    return points


def position(UE):
    # Gera a posição x, y de um UE com base em uma distribuição gaussiana, com valor esperado 50 e variância 20

    x = rd.gauss(50, 20)
    y = rd.gauss(50, 20)
    return x, y


def core_registration(UE, coverage_area, position_UE):
    # faz a checagem se o UE está na área de cobertuda do Core, e caso esteja, ele é registrado na rede

    x, y = position_UE
    area = coverage_area
    if x in len(area) and y in area[x]:
        return 1
    else:
        return -1
"""


def is_full(list_inactive, list_connected):
    if len(list_inactive) + len(list_connected) < 273:
        return False

    return True


def is_idle_full(list_idle):
    if len(list_idle) == 500:
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
        if state == 0:
            next = np.random.choice([0, 1], p=p1)
            if next == 1 and is_full(list_inactive, list_connected) is False:
                idle_to_connected(UE, list_connected)
            elif next == 0 and is_idle_full(list_idle) is False:
                list_idle.append(UE)
        elif state == 1:
            sleep(0.1)
            next = np.random.choice([0, 1], p=p2)
            if next == 0 and is_idle_full(list_idle) is False:
                connected_to_idle(UE, list_idle)
            elif next == 0 and is_idle_full(list_idle) is True:
                if is_full(list_inactive, list_connected) is False:
                    connected_to_inactive(UE, list_inactive)
            elif next == 1 and is_full(list_inactive, list_connected) is False:
                connected_to_inactive(UE, list_inactive)
            elif next == 1 and is_full(list_inactive, list_connected) is True:
                if is_idle_full(list_idle) is False:
                    connected_to_idle(UE, list_idle)
        elif state == 2:
            sleep(0.8)
            next = np.random.choice([0, 1], p=p3)
            if next == 1 and is_full(list_inactive, list_connected) is False:
                inactive_to_connected(UE, list_connected)
            elif next == 1 and is_full(list_inactive, list_connected) is True:
                if is_idle_full(list_idle) is False:
                    inactive_to_idle(UE, list_idle)
            elif next == 0 and is_idle_full(list_idle) is False:
                inactive_to_idle(UE, list_idle)
            elif next == 0 and is_idle_full(list_idle) is True:
                if is_full(list_inactive, list_connected) is False:
                    inactive_to_connected(UE, list_connected)
    else:
        '''
        p = [idle-> idle, idle-> connected], [connected->idle, connected-> inactive], [inactive-> idle, inactive-> connected]
        '''
        p1= [0.01, 0.99]
        p2 = [0.1, 0.9]
        p3 = [0.2, 0.8]
        if state == 0:
            next = np.random.choice([0, 1], p=p1)
            if next == 1 and is_full(list_inactive, list_connected) is False:
                idle_to_connected(UE, list_connected)
            elif next == 0 and is_idle_full(list_idle) is False:
                list_idle.append(UE)
        elif state == 1:
            sleep(0.8)
            next = np.random.choice([0, 1], p=p2)
            if next == 0 and is_idle_full(list_idle) is False:
                connected_to_idle(UE, list_idle)
            elif next == 1 and is_full(list_inactive, list_connected) is False:
                connected_to_inactive(UE, list_inactive)
        elif state == 2:
            sleep(0.01)
            next = np.random.choice([0, 1], p=p3)
            if next == 1 and is_full(list_inactive, list_connected) is False:
                inactive_to_connected(UE, list_connected)
            elif next == 0 and is_idle_full(list_idle):
                inactive_to_idle(UE, list_idle)


UEs_idle = []
UEs_connected = []
UEs_inactive = []
states = [UEs_idle, UEs_connected, UEs_inactive]
y = []
z = []
w = []
x = []


while is_idle_full(UEs_idle) is False:
    UEs_idle.append(rd.randint(0, 1))  # Entrada de usuários na rede, 0 -> baixo consumo, 1 -> alto consumo
    if len(UEs_idle) > 10:
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
