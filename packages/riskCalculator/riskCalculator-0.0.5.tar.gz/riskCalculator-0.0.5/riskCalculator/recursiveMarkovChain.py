from riskCalculator.probabilityOfLosses import *


def recursiveMarkovChain(attackers: int, defenders: int, memoryArray, baseCase):
    if (defenders <= 0 or attackers <= 0):
        return baseCase(attackers)

    rememberedValue = memoryArray[attackers-1][defenders-1]
    if (rememberedValue != None):
        return rememberedValue

    attackDie = min(attackers, 3)
    defenseDie = min(defenders, 2)

    # expected value of the chain(a,d) = \sum_l P(l)*chain(a-l, d - dd + l)
    result = sum(
        [
            # the probability of losses
            probabilityOfLosses(attackDie, defenseDie, losses)
            # the expected value of the scenario after losses
            * recursiveMarkovChain(attackers - losses, defenders - defenseDie + losses, memoryArray, baseCase)
            for losses in range(min(attackDie, defenseDie) + 1)
        ]
    )

    memoryArray[attackers-1][defenders-1] = result
    return result
