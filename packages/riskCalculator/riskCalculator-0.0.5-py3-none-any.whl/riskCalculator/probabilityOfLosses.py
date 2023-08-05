def probabilityOfLosses(attackDie: int, defenseDie: int, losses: int):
    if (defenseDie == 0):
        return 0 if losses > 0 else 1
    if (defenseDie == 1):
        return probabilityOfXLossesOneDefender(attackDie, losses)
    return probabilityOfXLossesTwoDefenders(attackDie, losses)


def probabilityOfXLossesOneDefender(attackDie: int, losses: int):
    if (losses > 1):
        return 0
    if (losses == 0):
        return [0.4167, 0.5787, 0.6597][attackDie - 1]
    return [0.5833, 0.4213, 0.3403][attackDie - 1]


def probabilityOfXLossesTwoDefenders(attackDie: int, losses: int):
    if (losses == 0):
        return [0.2546, 0.2276, 0.3717][attackDie - 1]
    if (losses == 1):
        return [0.7454, 0.3241, 0.3358][attackDie - 1]
    return [0, 0.4483, 0.2926][attackDie - 1]
