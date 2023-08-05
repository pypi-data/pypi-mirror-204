def probabilityOfLosses(attackDie: int, defenseDie: int, losses: int):
    if (defenseDie == 0):
        return 0
    if (defenseDie == 1):
        return probabilityOfXLossesOneDefender(attackDie, losses)
    return probabilityOfXLossesTwoDefenders(attackDie, losses)


def probabilityOfXLossesOneDefender(attackDie: int, losses: int):
    if (losses == 0):
        return [0.417, 0.579, 0.66][attackDie - 1]
    return [0.583, 0.421, 0.34][attackDie - 1]


def probabilityOfXLossesTwoDefenders(attackDie: int, losses: int):
    if (losses == 0):
        return [0.255, 0.228, 0.372][attackDie - 1]
    if (losses == 1):
        return [0, 0.448, 0.292][attackDie - 1]
    return [0.745, 0.448, 0.336][attackDie - 1]
