# Risk
A simple python script for calculating the likely outcome of a Risk battle.

## Arguments
The script takes in the number of `attackers` and `defenders` as arguments. 
```sh
yarn risk <attackers> <defenders>
```

## Returns
The likelihood of victory and the average number of survivors (attackers).
```sh
Likelihood of victory 57.7% with 2.7 survivors on average.
```

## Usage
I have an 11 stack, should I attack that 10 stack? Let's find out!

We can't attack with all 11 stacks, because we have to leave one behind. So when we attack we'll have 10 attacking into 10:

```sh
./risk --attackers 10 --defenders 10
```

We see the following output:
```sh
Likelihood of victory 57.7% with 2.7 survivors on average.
```

The script tells us we have a 57.7% chance of winning, and on average we'll have 2.7 survivors (3.7 if you include the stack left behind).


## build & deploy
bump version in `setup.py`
`g a . && g c -m "bump version"`
`python setup.py sdist bdist_wheel`
`twine upload dist/* --skip-existing`