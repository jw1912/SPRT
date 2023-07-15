# GSPRT

GSPRT stands for Generalised SPRT.

## Modelling as a Trinomial

Chess games can have 3 outcomes (duh) so we can model as a trinomial, $w$, $l$
and $d = 1 - w - l$ are the win, loss and draw probabilities, respectively.

Suppose our test has $N$ samples, with $W$ wins, $L$ losses and $D$ draws, where
obviously $N = W + L + D$, then the estimated probabilities are $w = W / N$,
$l = L / N$ and $d = D / N$.

Now define the random variable

$$
X = \frac{W + D / 2}{N}
$$

Using some basic properties of multinomial distributions[^TRINOM], it follows that

$$
\mathbb{E}[X] = w + d / 2
$$

and

$$
\mathbb{E}[X^2] = \frac{1}{N^2} (\mathbb{E}[W^2] +\mathbb{E}[WD] + \mathbb{E}[D^2] / 4)
$$

$$
\mathbb{E}[W^2] = N w (1 - w) + N^2 w^2
$$

$$
\mathbb{E}[D^2] = N d (1 - d) + N^2 d^2
$$

$$
\mathbb{E}[WD] = N (N - 1) w d
$$

therefore

$$
\begin{align*}
\mathbb{E}[X^2] & = \frac{1}{N} (
    w - w^2 + d / 4 - d^2 / 4 - w d + N(w^2 + d^2 / 4 + w d)
) \\
& = \frac{1}{N} (w + d / 4) + (1 - \frac{1}{N}) (w + d / 2)^2
\end{align*}
$$

and so finally

$$
var(X) = \frac{1}{N} (w + d/4 - (w + d/2)^2)
$$

## How does GSPRT work?

GSPRT[^GSPRT] works essentially the same as SPRT, with a different Log-Likelihood Ratio (LLR) calculation,
instead replacing it with the Generalised Likelihood Ratio.

Luckily we don't need to worry about this, as there is an approximate formula for the LLR[^GSPRT_APPROX]:

$$
LLR = \frac{(p_1 - p_0)(2X - p_0 - p_1)}{2var(X)}
$$

where $X$ and $var(X)$ are based on the games played so far, and

$$
p_i = \frac{1}{1 + 10^{-e_i / 400}}
$$

[^TRINOM]: [The Trinomial Distribution](https://webspace.maths.qmul.ac.uk/i.goldsheid/MTH5118/Notes6-09.pdf)

[^GSPRT]: [Generalized Sequential Probability Ratio Test for Separate Families of Hypotheses](http://stat.columbia.edu/~jcliu/paper/GSPRT_SQA3.pdf)

[^GSPRT_APPROX]: [A Practical Introduction to the GSPRT](https://hardy.uhasselt.be/Toga/GSPRT_approximation.pdf)