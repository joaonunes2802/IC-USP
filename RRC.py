"""
This file is responsible for implementation of NR RRC in context of 5G Network using
Markov Chains to model RRC states, which are, idle, connected and inactive states.
"""
import random as rd


def sorteio_idle(list_idle):
    # Sorteia um UE aleatoriamente que se encontra em uma posição entre 1 e 550
    # O limite de UE em idle é 550

    index = rd.randint(1, len(list_idle) - 1)
    UE = list_idle.pop(index)
    return UE


def sorteio_connected(list_connected):
    # Sorteia um UE aleatoriamente que se encontra em uma posição entre 1 e o tamanho atual da lista de UE connected
    # O limite de UE connected é 273

    index = rd.randint(1, len(list_connected) - 1)
    UE = list_connected.pop(index)
    return UE


def sorteio_inactive(list_inactive):
    # Sorteia aleatoriamente um UE que está em inactive
    # O limite de UE em inactive é 279

    index = rd.randint(1, len(list_inactive) - 1)
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


def transition_matrix(actual_state):
    # linha 1 (index 0) - idle
    # linha 2 (index 1)- connected
    # linha 3 (index 2)- inactive

    # O usuário só tem chance de permanecer no mesmo estado se estiver em idle
    # A probabilidade de permanecer em qualquer outro estado é 0, supõem-se que ao ser sorteado, o UE deve fazer algo.
    # O UE que está em idle não pode ir direto para inactive, ele deve antes passar pelo connected
    # Logo, a probabilidade de um UE em idle ir para o connected ou permanecer em idle é 0.5
    # A probabilidade de um UE se mover para um estado permitido é 0.5

    # P(idle -> idle) = 0.5 ; a11
    # P(idle -> connected) = 0.5; a12
    # P(idle -> inactive) = 0; a13
    # P(inactive -> idle) = 0.5; a21
    # P(inactive -> inactive) = 0; a22
    # P(inactive -> connected) = 0.5; a23
    # P(connected -> idle) = 0.5; a31
    # P(connected -> inactive) = 0.5; a32
    # P(connected -> connected) = 0; a33

    matrix = [[0.5, 0.5, 0], [0.5, 0, 0.5], [0.5, 0.5, 0]]
    next_state = rd.randint(1, 2)
    prob = matrix[actual_state][next_state]
    return next_state, prob


def inactive(UE, list_idle, list_connected):
    # Após o sorteio, verifica se o UE que passar para o connected, permanecer em iactive, ou ir para idle

    next_state, prob = transition_matrix(1)
    if prob == 0:  # Deseja permanecer em inactive, nesse caso, como o seu tempo esgotou, vai para idle
        inactive_to_idle(UE, list_idle)
    else:
        if next_state == 0:
            inactive_to_idle(UE, list_idle)
        else:
            inactive_to_connected(UE, list_connected)


def idle(UE, list_connected, idle_list):
    # Após o sorteio, verifica se o UE que passar para o connected ou permanecer idle

    next_state, prob = transition_matrix(0)
    if prob == 0:   # deseja ir de idle para inactive, o que é proibido
        idle_list.append(UE)
    else:
        if next_state == 0:
            idle_list.append(UE)  # Usuario deseja permanecer em idle
        else:
            idle_to_connected(UE, list_connected)


def connected(UE, list_idle, list_inactive):
    # Após o sorteio, verifica se o UE que passar para o idle, ir para o inactive ou permanecer em connected

    next_state, prob = transition_matrix(2)
    if prob == 0:  # Deseja permancer em connected, nesse caso, ele deve ir para inactive
        connected_to_inactive(UE, list_inactive)
    else:
        if next_state == 0:
            connected_to_idle(UE, list_idle)
        else:
            connected_to_inactive(UE, list_inactive)


UEs_idle = []
UEs_connected = []
UEs_inactive = []

for t_execucao in range(1, 1000):
    UEs_idle.append(range(2))
    if len(UEs_idle) > 10:
        UEI_sorteado = sorteio_idle(UEs_idle)
        idle(UEI_sorteado, UEs_connected, UEs_idle)

    if len(UEs_connected) > 50:
        UEC_sorteado = sorteio_connected(UEs_connected)
        connected(UEC_sorteado, UEs_idle, UEs_inactive)

    if len(UEs_inactive) > 279:
        UEIN_sorteado = sorteio_inactive(UEs_inactive)
        inactive(UEIN_sorteado, UEs_idle, UEs_connected)

    print(f"Usuarios idle = {len(UEs_idle)}, Usuarios connected = {len(UEs_connected)}, Usuarios inactive = {len(UEs_inactive)}")


# Problema: Sair do inactive
