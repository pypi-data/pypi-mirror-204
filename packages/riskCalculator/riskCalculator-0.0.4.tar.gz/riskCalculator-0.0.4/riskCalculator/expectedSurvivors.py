from riskCalculator.recursiveMarkovChain import *


def expectedSurvivors(attackers: int, defenders: int, expectedSurvivorsArray):
    return recursiveMarkovChain(
        attackers,
        defenders,
        expectedSurvivorsArray,
        # if there are no defenders then all attackers survive
        lambda attackers: attackers if attackers > 0 else 0
    )
