# SPRT

This repo contains:
- a scipt to calculate SPRT results, as per OpenBench's method
- derivation/explanations of
    - [SPRT](SPRT.md) (used by OpenBench and CuteChess)
    - [GSPRT](GSPRT.md) (of which a more developed method is used by Fishtest)

All of this is, of course, in the context of chess. Some familiarity with what hypothesis testing does is assumed for the explanantions.

### Running Script
Run `python3 sprt.py --help` for a full list of options.

#### Sample usage
```
python3 sprt.py --wins 4307 --losses 4063 --draws 8620 --elo0 0 --elo1 3
> LLR: 2.47 (-2.94, 2.94)
> Continue Playing
```

