from riskCalculator.recursiveMarkovChain import *


def likelihoodOfVictory(attackers: int, defenders: int, likelihoodOfVictoryArray):
    return recursiveMarkovChain(
        attackers,
        defenders,
        likelihoodOfVictoryArray,
        # if there are no defenders and any attackers they win with probability 1
        lambda attackers: 1 if attackers > 0 else 0
    )
