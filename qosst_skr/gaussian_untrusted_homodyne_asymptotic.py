# qosst-skr - Secret Key Rate computation module of the Quantum Open Software for Secure Transmissions.
# Copyright (C) 2021-2024 Yoann Piétri

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Calulator for Gaussian Modulation with Untrusted detector and Homodyne detection using the asymptotic regime.
"""
from math import log2

from qosst_core.skr_computations import BaseCVQKDSKRCalculator

from qosst_skr.utils import g


# Disable invalid names to avoid raising errors with Va, T, xi, etc...
# pylint: disable=invalid-name, too-few-public-methods
class GaussianUntrustedHomodyneAsymptotic(BaseCVQKDSKRCalculator):
    """
    This assumes:

    * Gaussian Modulation
    * Untrusted detector
    * Homodyne Detection
    * Asymptotic key rate

    References:
    Leverrier, A. (2009). Theoretical study of continuous-variable quantum key distribution. (Doctoral dissertation, Telécom ParisTech).
    Raúl García-Patrón, & Nicolas J. Cerf (2006). Unconditional Optimality of Gaussian Attacks against Continuous-Variable Quantum Key Distribution. Physical Review Letters, 97(19).
    Miguel Navascués, Fredéric Grosshans, & Antonio Acín (2006). Optimality of Gaussian Attacks in Continuous-Variable Quantum Cryptography. Physical Review Letters, 97(19).
    """

    @staticmethod
    def skr(**kwargs) -> float:
        """
        This method computes the secret key rate in the case of the untrusted homdyne detector, with Gaussian modulation,
        in the asymptotic scenario.

        This method actually get the arguments and pass them to the _skr method that actually computes the SKR.

        Args:
            Va (float): Alice's variance of modulation (in SNU).
            T (float): transmittance of the channel.
            xi (float): excess noise of the channel (in SNU).
            beta (float, optional): efficiency of the reconciliation. Default to 0.95.

        Returns:
            float: secret key rate in bits per symbol.
        """
        Va = kwargs.pop("Va")
        T = kwargs.pop("T")
        xi = kwargs.pop("xi")
        beta = kwargs.pop("beta")
        return GaussianUntrustedHomodyneAsymptotic._skr(Va, T, xi, beta)

    @staticmethod
    def _skr(Va: float, T: float, xi: float, beta: float) -> float:
        """
        Compute the SKR as I_ab - X_be by calling the _iab and _holevo_bound method.

        If the key rate is less than 0, return 0.

        Args:
            Va (float): Alice's variance of modulation (in SNU).
            T (float): transmittance of the channel.
            xi (float): excess noise of the channel (in SNU).
            beta (float): efficiency of the reconciliation.

        Returns:
            float: secret key rate in bits per symbol.
        """
        s = GaussianUntrustedHomodyneAsymptotic._iab(
            Va, T, xi, beta
        ) - GaussianUntrustedHomodyneAsymptotic._holevo_bound(Va, T, xi)
        if s > 0:
            return s
        return 0

    @staticmethod
    def _iab(Va: float, T: float, xi: float, beta: float) -> float:
        """
        Compute the information shared by Alice and Bob in the case of the untrusted homodyne detector, with Gaussian modulation,
        in the asymptotic scenario.

        Args:
            Va (float): Alice's variance of modulation (in SNU).
            T (float): transmittance of the channel.
            xi (float): excess noise of the channel (in SNU).
            beta (float): efficiency of the reconciliation.

        Returns:
            float: information shared by Alice and Bob in bits per symbol.
        """
        return beta * 0.5 * log2(1 + T * Va / (1 + T * xi))

    @staticmethod
    def _holevo_bound(Va: float, T: float, xi: float) -> float:
        """
        Compute the Holevo bound on the information between Bob and Eve in the case of the untrusted homodyne detector, with Gaussian modulation,
        in the asymptotic scenario.

        Args:
            Va (float): Alice's variance of modulation (in SNU).
            T (float): transmittance of the channel.
            xi (float): excess noise of the channel (in SNU).

        Returns:
            float: Holevo's bound on the information between Eve and Bob in bits per symbol.
        """
        V = Va + 1
        delta = V**2 + (1 + T * (V - 1) + T * xi) ** 2 - 2 * T * (V**2 - 1)
        D = ((1 + T * (V - 1) + T * xi) * V - T * (V**2 - 1)) ** 2
        nu_1 = 0.5 * (delta + (delta**2 - 4 * D) ** 0.5)
        nu_2 = 0.5 * (delta - (delta**2 - 4 * D) ** 0.5)
        nu_3 = V * (V - (T * (V**2 - 1)) / (1 + T * (V - 1) + T * xi))
        return g((nu_1 - 1) / 2) + g((nu_2 - 1) / 2) - g((nu_3 - 1) / 2)
