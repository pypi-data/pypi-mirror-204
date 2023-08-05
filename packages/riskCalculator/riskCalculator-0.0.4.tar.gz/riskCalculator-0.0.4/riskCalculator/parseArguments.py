from argparse import *


def parseArguments(defaultAttackers: int, defaultDefenders: int):
    parser = ArgumentParser(description="arguments for risk calculation")
    parser.add_argument(
        '--attackers',
        metavar="a",
        type=int,
        help='number of attackers',
        default=defaultAttackers,
        required=False
    )
    parser.add_argument(
        '--defenders',
        metavar="d",
        type=int,
        help='number of defenders',
        default=defaultDefenders,
        required=False
    )
    parser.add_argument(
        '--read',
        action=BooleanOptionalAction,
        dest="read",
        help="should use saved results"
    )
    parser.add_argument(
        '--write',
        action=BooleanOptionalAction,
        dest="write",
        help="should save results"
    )
    parser.add_argument(
        '--recursion-limit',
        type=int,
        default=1000,
        metavar="R",
        dest="recursionLimit",
        help="recursion limit, default 1000"
    )

    return parser.parse_args()
