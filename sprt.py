from math import pow, sqrt, log, log10, copysign, pi
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


def expected_score(x: float) -> float:
    return 1.0 / (1.0 + pow(10, -x / 400.0))


def adj_probs(b: BayesElo) -> Probability:
    win = expected_score(-b.draw + b.elo)
    loss = expected_score(-b.draw - b.elo)
    return Probability(win, loss, 1 - win - loss)


def scale(draw_elo: float) -> float:
    x = pow(10, -draw_elo / 400)
    return 4 * x / pow(1 + x, 2)


def sprt(
        wins: int,
        losses: int,
        draws: int,
        elo0: float,
        elo1: float,
        cutechess: bool = False
        ) -> float:
    if wins == 0 or losses == 0 or draws == 0:
        return 0.0

    total = wins + draws + losses

    probs = Probability(wins / total, losses / total, draws / total)

    draw_elo = 200 * log10((1 - 1 / probs.win) * (1 - 1 / probs.loss))

    # cutechess applies a draw elo based scaling
    s = 1
    if cutechess:
        s = scale(draw_elo)

    b0 = BayesElo(elo0 / s, draw_elo)
    b1 = BayesElo(elo1 / s, draw_elo)

    p0 = adj_probs(b0)
    p1 = adj_probs(b1)

    return wins * log(p1.win / p0.win) \
        + losses * log(p1.loss / p0.loss) \
        + draws * log(p1.draw / p0.draw)


def gsprt(
        wins: int,
        losses: int,
        draws: int,
        elo0: float,
        elo1: float,
        _=None
        ) -> float:
    p0 = expected_score(elo0)
    p1 = expected_score(elo1)

    N = wins + losses + draws
    if N == 0:
        return 0.0

    w = wins / N
    d = draws / N

    X = w + d / 2
    varX = (w + d / 4 - pow(X, 2)) / N

    return (p1 - p0) * (2 * X - p0 - p1) / (2 * varX)


def erf_inv(x):
    a = 8 * (pi - 3) / (3 * pi * (4 - pi))
    y = log(1 - x * x)
    z = 2 / (pi * a) + y / 2
    return copysign(sqrt(sqrt(z * z - y / a) - z), x)


def phi_inv(p):
    return sqrt(2)*erf_inv(2*p-1)


def elo(score: float) -> float:
    if score <= 0 or score >= 1:
        return 0.0
    return -400 * log10(1 / score - 1)


def elo_wld(wins, losses, draws):
    # win/loss/draw ratio
    N = wins + losses + draws
    if N == 0:
        return (0, 0, 0)

    p_w = float(wins) / N
    p_l = float(losses) / N
    p_d = float(draws) / N

    mu = p_w + p_d/2
    stdev = sqrt(p_w*(1-mu)**2 + p_l*(0-mu)**2 + p_d*(0.5-mu)**2) / sqrt(N)

    # 95% confidence interval for mu
    mu_min = mu + phi_inv(0.025) * stdev
    mu_max = mu + phi_inv(0.975) * stdev

    return (elo(mu_min), elo(mu), elo(mu_max))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="llr calculator")
    parser.add_argument(
        '-w', '--wins', type=int, help="number of wins", default=0)
    parser.add_argument(
        '-l', '--losses', type=int, help="number of losses", default=0)
    parser.add_argument(
        '-d', '--draws', type=int, help="number of draws", default=0)
    parser.add_argument(
        '-e0', '--elo0', type=float, help="lower elo", default=0)
    parser.add_argument(
        '-e1', '--elo1', type=float, help="upper elo", default=5)
    parser.add_argument(
        '-a', '--alpha', type=float, help="allowed margin of error for Type 1",
        default=0.05)
    parser.add_argument(
        '-b', '--beta', type=float, help="allowed margin of error for Type 2",
        default=0.05)
    parser.add_argument(
        '--cutechess', action="store_true", help="use CuteChess draw scaling")
    parser.add_argument(
        '--gsprt', action="store_true", help="run GSPRT calculation instead")
    args = parser.parse_args()

    func = gsprt if args.gsprt else sprt

    llr = func(
        args.wins,
        args.losses,
        args.draws,
        args.elo0,
        args.elo1,
        args.cutechess,
    )

    lower = log(args.beta / (1 - args.alpha))
    upper = log((1 - args.beta) / args.alpha)

    if llr >= upper:
        message = "H1 Accepted"
    elif llr <= lower:
        message = "H0 Accepted"
    else:
        message = "Continue Playing"

    e1, e2, e3 = elo_wld(args.wins, args.losses, args.draws)
    print(f"ELO: {e2:.3} +- {(e3 - e1) / 2:.3} [{e1:.3}, {e3:.3}]")
    print(f"LLR: {llr:.3} [{args.elo0}, {args.elo1}] ({lower:.3}, {upper:.3})")
    print(message)
