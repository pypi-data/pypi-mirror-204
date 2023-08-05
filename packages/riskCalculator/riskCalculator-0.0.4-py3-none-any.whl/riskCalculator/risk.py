import sys
from riskCalculator.parseArguments import *
from riskCalculator.readWriteData import *
from riskCalculator.likelihoodOfVictory import *
from riskCalculator.expectedSurvivors import *


def risk(defaultAttackers: int = 0, defaultDefenders: int = 0):
    args = parseArguments(defaultAttackers, defaultDefenders)
    attackers = args.attackers
    defenders = args.defenders

    # initialise variables
    maxDice = max(attackers, defenders, 200 if args.write else 1)
    expectedSurvivorsArray = [[None]*maxDice for x in range(maxDice)]
    likelihoodOfVictoryArray = [[None]*maxDice for x in range(maxDice)]
    sys.setrecursionlimit(args.recursionLimit)

    if (args.read):
        readData("expectedSurvivors.txt", expectedSurvivorsArray)
        readData("likelihoodOfVictory.txt", likelihoodOfVictoryArray)

    # calculate expected result and chance
    chance = round(
        likelihoodOfVictory(
            attackers, defenders, likelihoodOfVictoryArray
        ) * 100,
        1
    )

    survivors = round(
        expectedSurvivors(
            attackers, defenders, expectedSurvivorsArray
        ),
        2
    )

    # inform user
    print(
        "Likelihood of victory " + str(chance) + "% with "
        + str(survivors) + " survivors on average."
    )

    if (args.write):
        writeData("expectedSurvivors.txt", expectedSurvivorsArray)
        writeData("likelihoodOfVictory.txt", likelihoodOfVictoryArray)

    return [chance, survivors]
