# GSPRT

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

Some useful properties of the trinomial distribution are derived
[here](https://webspace.maths.qmul.ac.uk/i.goldsheid/MTH5118/Notes6-09.pdf),
from which it follows that

$$
\mathbb{E}[X] = w + d / 2
$$

And now, for calculating the variance in $X$:

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

Therefore

$$
\begin{align*}
\mathbb{E}[X^2] & = \frac{1}{N} (
    w - w^2 + d / 4 - d^2 / 4 - w d + N(w^2 + d^2 / 4 + w d)
) \\
& = \frac{1}{N} (w + d / 4) + (1 - \frac{1}{N}) (w + d / 2)^2
\end{align*}
$$