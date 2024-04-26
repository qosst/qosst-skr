# Understanding the computation of SKR in CV-QKD

## Secret key rate in CV-QKD

The secret key rate, in CV-QKD, is a measure of the number of secret bits that can be extracted from a symbol. The way to compute it depends on the security assumptions that are considered. It usually takes the form of the Devetak-Winter formula

```{math}
K = \beta I_{AB} - \chi_{BE}
```

where {math}`0\leq \beta \leq 1` is the reconciliation efficiency, usually more than 90%, and {math}`I_{AB}` and {math}`\chi_{BE}`, respectively the shared information between Alice and Bob and the Holevo bound on the maximal information shared between Bob and Eve are two quantities that, in the Gaussian case, depends on {math}`V_A, T, \xi, \eta, V_{el}`.

The formulas for both {math}`I_{AB}` and {math}`\chi_{BE}` depends on the type of detection (homodyne or heterodyne) and if the detector is trusted or not (*i.e.* if some part of the losses and noise are considered trusted on Bob side).

The analysis in the discrete modulation case is more complicated, and, at the date of writing this, not complete.

Finally, those formulas usually takes as an assumption that the number of symbols is infinite, or equivalently, that we can perfectly estimate {math}`\xi` and {math}`T` which is, in real life, not true. For this reason, it is necessary to remove part of this value when considering finite size effect.

## Link between parameters estimation and secret key rate calculations

The idea of the software is that the output of the parameter estimations step should output the required parameters for the secret key rate calculator. However, in the current state of the software, we only focus on secret key rate calculators that depends on the following parameters: {math}`V_A, T, \xi, \eta, V_{el}, \beta`, namely Alice modulation strength, transmittance, excess noise, detector efficiency, detector electronic noise and reconciliation efficiency. This is one of the current limitations of the software, especially if one wants to use for instance new proofs for discrete modulation.

## Using calculators

The calculators inherit from {py:class}`qosst_core.skr_computations.BaseCVQKDSKRCalculator` and must implement a static `skr` command. The parameters that are needed should be looked in the configuration of the specific calculator.

Here is an example with the {py:class}`~qosst_skr.gaussian_trusted_heterodyne_asymptotic.GaussianTrustedHeterodyneAsymptotic` calculator:

```{code-block} python

from qosst_skr import GaussianTrustedHeterodyneAsymptotic

skr = GaussianTrustedHeterodyneAsymptotic.skr(Va=1, T=0.5, xi=0.01, eta=0.8, Vel=0.1, beta=0.95)
```