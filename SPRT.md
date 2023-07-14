# SPRT

Both OpenBench and CuteChess use Bayesian Elo estimates (rather than the classical formula),
in order to "properly" adjust for draws, indeed CuteChess takes this even further by applying
an additional scaling based on draw rate in its SPRT calculation.

## Modelling Elo using [BayesElo](https://www.remi-coulom.fr/Bayesian-Elo/#theory)

Elo is primarily based on a sigmoid scale
$$
f(x) = \frac{1}{1 + 10^{-x/400}}
$$

Given a rating difference $x$, the expected probabilites of wins, losses and draws are
given by

$$
\begin{align*}
w & = f(-y + x) \\
l & = f(-y - x) \\
d & = 1 - w - l
\end{align*}
$$

respectively, where $y$ is an adjustment based on the draw ratio, given by

$$
y = 200 \log_{10}((\frac{1}{w'} - 1) * (\frac{1}{l'} - 1))
$$

where $w'$ and $l'$ are the win and loss probabilities from a large sample of games.

### Where does the draw adjustment come from?
The classical elo formula gives the expected score, $s$, of a player with a relative elo advantage over an opponent of $e$, as

$$
s = f(e)
$$

Rearranging this to work out instead the expected elo advantage, given score, gives

$$
e = -400 \log_{10}(\frac{1}{s} - 1)
$$

and now it's easy to see that the draw elo is given by

$$
y = -\frac{1}{2} (e_w + e_l)
$$

where $e_w$ is the elo advantage from the perspective of the first player, given all draws
are counted as losses, and similarly $e_l$ is the elo advantage from the perspective of the
opponent, where all draws are counted as losses.

## How SPRT actually works
