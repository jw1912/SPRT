import math
from dataclasses import dataclass

@dataclass
class Probability:
    win: float
    loss: float
    draw: float

@dataclass
class BayesElo:
    elo: float
    draw: float

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.pow(10, x / 400.0))

def adj_probs(b: BayesElo) -> Probability:
    win  = sigmoid(b.draw - b.elo)
    loss = sigmoid(b.draw + b.elo)
    return Probability(win, loss, 1 - win - loss)

def sprt(wins: int, losses: int, draws: int, elo0: float, elo1: float) -> float:
    total = wins + draws + losses
    probs = Probability(wins / total, losses / total, draws / total)

    draw_elo = 200 * math.log10((1 - 1 / probs.win) * (1 - 1 / probs.loss))

    b0 = BayesElo(elo0, draw_elo)
    b1 = BayesElo(elo1, draw_elo)

    p0 = adj_probs(b0)
    p1 = adj_probs(b1)

    return wins  * math.log(p1.win  / p0.win ) \
        + losses * math.log(p1.loss / p0.loss) \
        + draws  * math.log(p1.draw / p0.draw)

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="llr calculator")
    parser.add_argument('-w', '--wins', type=int, help="number of wins")
    parser.add_argument('-l', '--losses', type=int, help="number of losses")
    parser.add_argument('-d', '--draws', type=int, help="number of draws")
    parser.add_argument('-e0', '--elo0', type=float, help="lower elo")
    parser.add_argument('-e1', '--elo1', type=float, help="upper elo")
    args = parser.parse_args()

    llr = sprt(
        args.wins,
        args.losses,
        args.draws,
        args.elo0,
        args.elo1
    )

    print(f"llr = {llr}")