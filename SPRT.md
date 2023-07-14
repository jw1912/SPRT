# SPRT

Both OpenBench and CuteChess use Bayesian Elo estimates (rather than the classical formula),
in order to "properly" adjust for draws, indeed CuteChess takes this even further by applying
an additional scaling based on draw rate in its SPRT calculation.

## Modelling Elo using [BayesElo](https://www.remi-coulom.fr/Bayesian-Elo/#theory)

Elo is primarily based on a sigmoid scale

$$
f(x) = \frac{1}{1 + 10^{-x/400}}
$$

In Bayesian Elo, given a rating difference $x$, the expected probabilites of wins, losses and
draws are given by

$$
\begin{align}
w & = f(-y + x) \\
l & = f(-y - x) \\
d & = 1 - w - l
\end{align}
$$

respectively, where $y$ is an adjustment based on the draw ratio, called the *draw elo*, given by

$$
y = 200 \log_{10}((\frac{1}{w'} - 1) * (\frac{1}{l'} - 1))
$$

where $w'$ and $l'$ are the win and loss probabilities from a large sample of games.

### Where does the draw elo come from?

*Note: This is more of an educated guess.*

The classical elo formula gives the expected score, $s$, of a player with a relative elo advantage
over an opponent of $e$, as

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

So you have your `old` engine, and have made a change, resulting in a `new` engine.

Now, you make two a null and alternative hypothesis about the elo change $\Delta e$,
as with any other statistical test:
- H0: $\Delta e = e_0$
- H1: $\Delta e = e_1$

You of course have to decide on a margin of error, otherwise your test will never end;
the standard choices are $\alpha = 0.05$ and $\beta = 0.05$, which corresponds to a test
that concludes with 95% certainty.

These values define two bounds, $a = \log(\frac{\beta}{1 - \alpha})$ and
$b = \log(\frac{1 - \beta}{\alpha})$. With the two aforementioned values for $\alpha$ and $\beta$
this gives $a = -2.94$ and $b = 2.94$.

Now we start playing games.

After each game, we calculate the *Log Likelihood Ratio* (LLR) of the two hypotheses, and if it
exceeds $b$ we accept H1, if it is lower than $a$ we accept H0, and otherwise we continue
playing.

## Calculating LLR

### Definition

The formula for LLR is as follows

$$
LLR = LL(e_1) - LL(e_0)
$$

where $LL(x)$ is the *Log-Likelihood* of elo $x$.

Given a random variable $\mathbf{X} = (X_1, X_2, ...)$ with some distribution with parameter
$\theta$, the Likelihood Function of $\mathbf{X}$, based on a sample with outcome
$\mathbf{X} = \mathbf{x}$, is

$$
\mathcal{L}(\theta) = P(\mathbf{X} = \mathbf{x} \vert \theta)
$$

i.e. the probability of achieving outcome $\mathbf{x}$ under parameter $\theta$.

And then the Log-Likelihood is just the natural logarithm of this:

$$
LL(\theta) = \log(P(\mathbf{X} = \mathbf{x} \vert \theta))
$$

### For Chess

Now let's calculate the Log-Likelihood of the outcome after $N$ games, say we have
$W$ wins, $L$ losses and $D = N - W - L$ draws, with an elo parameter of $e$.

Firstly we calculate the draw elo, as above, using our games

$$
y = 200 \log_{10}((\frac{1}{W / N} - 1) * (\frac{1}{L / N} - 1))
$$

Then we use equations $(1) - (3)$, where $x = e$, to calculate our win, loss and draw
probabilities

$$
\begin{align*}
w & = f(-y + e) \\
l & = f(-y - e) \\
d & = 1 - w - l
\end{align*}
$$

We model the outcome as a trinomial distribution, so

$$
P(W, L, D \vert e) = \frac{N!}{W! L! D!} w^W l^L d^D
$$

then

$$
\begin{align*}
LL(e) & = \log(P(W, L, D \vert e)) \\
    & = \log(\frac{N!}{W! L! D!} w^W l^L d^D) \\
    & = W \log(w) + L \log(l) + D \log(d) + \log(\frac{N!}{W! L! D!})
\end{align*}
$$

and so, calculating probabilities $w_1, l_1, d_1$ for $e_1$ and $w_0, l_0, d_0$ for $e_0$,
we get a formula for the Log-Likelihood Ratio

$$
\begin{align*}
LLR & = LL(e_1) - LL(e_2) \\
    & = W \log(w_1) + L \log(l_1) + D \log(d_1) + \log(\frac{N!}{W! L! D!}) \\
    & \quad \quad - W \log(w_0) - L \log(l_0) - D \log(d_0) - \log(\frac{N!}{W! L! D!}) \\
    & = W \log(w_1 / w_0) + L \log(l_1 / l_0) + D \log(d_1 / d_0)
\end{align*}
$$

## Why is it difficult to make a better SPRT?

At first glance, our hypotheses look dumb, why have inifitesimal points as the possible results
for the test, instead of something like
- H0: $\Delta e < e_0$
- H1: $\Delta e > e_1$

The answer to this is simple: calculate $P(W, L, D \vert e > e_0)$.

## Draw Scaling in CuteChess

Rather than using the raw $e_0$ and $e_1$, CuteChess scales each one by a factor dependent on
the draw elo.