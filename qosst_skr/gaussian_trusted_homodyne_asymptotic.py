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
Calulator for Gaussian Modulation with Trusted detector and Homodyne detection using the asymptotic regime.
"""
from math import log2

from qosst_core.skr_computations import BaseCVQKDSKRCalculator

from qosst_skr.utils import g


# Disable invalid names to avoid raising errors with Va, T, xi, etc...
# pylint: disable=invalid-name, too-few-public-methods
class GaussianTrustedHomodyneAsymptotic(BaseCVQKDSKRCalculator):
    """
    This assumes:

    * Gaussian Modulation
    * Trusted detector
    * Homodyne Detection
    * Asymptotic key rate

    References:
    Jérôme Lodewyck, Matthieu Bloch, Raúl García-Patrón, Simon Fossier, Evgueni Karpov, Eleni Diamanti, Thierry Debuisschert, Nicolas J. Cerf, Rosa Tualle-Brouri, Steven W. McLaughlin, & Philippe Grangier (2007). Quantum key distribution over 25km with an all-fiber continuous-variable system. Physical Review A, 76(4).
    """

    # pylint: disable=too-many-arguments
    @staticmethod
    def skr(**kwargs) -> float:
        """
        This method computes the secret key rate in the case of the trusted homdyne detector, with Gaussian modulation,
        in the asymptotic scenario.

        This method actually get the arguments and pass them to the _skr method that actually computes the SKR.

        Args:
            Va (float): Alice's variance of modulation (in SNU).
            T (float): transmittance of the channel.
            xi (float): excess noise of the channel (in SNU).
            eta (float): efficiency of the detector.
            Vel (float): electronic noise of the detector (in SNU).
            beta (float, optional): efficiency of the reconciliation. Default to 0.95.

        Returns:
            float: secret key rate in bits per symbol.
        """
        Va = kwargs.pop("Va")
        T = kwargs.pop("T")
        xi = kwargs.pop("xi")
        eta = kwargs.pop("eta")
        Vel = kwargs.pop("Vel")
        beta = kwargs.pop("beta")
        return GaussianTrustedHomodyneAsymptotic._skr(Va, T, xi, eta, Vel, beta)

    # pylint: disable=too-many-arguments
    @staticmethod
    def _skr(
        Va: float, T: float, xi: float, eta: float, Vel: float, beta: float
    ) -> float:
        """
        Compute the SKR as I_ab - X_be by calling the _iab and _holevo_bound method.

        If the key rate is less than 0, return 0.

        Args:
            Va (float): Alice's variance of modulation (in SNU).
            T (float): transmittance of the channel.
            xi (float): excess noise of the channel (in SNU).
            eta (float): efficiency of the detector.
            Vel (float): electronic noise of the detector (in SNU).
            beta (float): efficiency of the reconciliation.

        Returns:
            float: secret key rate in bits per symbol.
        """
        key_rate = GaussianTrustedHomodyneAsymptotic._iab(
            Va, T, xi, eta, Vel, beta
        ) - GaussianTrustedHomodyneAsymptotic._holevo_bound(Va, T, xi, eta, Vel)
        if key_rate > 0:
            return key_rate
        return 0

    # pylint: disable=too-many-arguments
    @staticmethod
    def _iab(
        Va: float, T: float, xi: float, eta: float, Vel: float, beta: float
    ) -> float:
        """
        Compute the information shared by Alice and Bob in the case of the trusted homodyne detector, with Gaussian modulation,
        in the asymptotic scenario.

        Args:
            Va (float): Alice's variance of modulation (in SNU).
            T (float): transmittance of the channel.
            xi (float): excess noise of the channel (in SNU).
            eta (float): efficiency of the detector.
            Vel (float): electronic noise of the detector (in SNU).
            beta (float): efficiency of the reconciliation.

        Returns:
            float: information shared by Alice and Bob in bits per symbol.
        """
        return beta * 0.5 * log2(1 + eta * T * Va / (1 + Vel + eta * T * xi))

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def _holevo_bound(Va: float, T: float, xi: float, eta: float, Vel: float) -> float:
        """
        Compute the Holevo bound on the information between Bob and Eve in the case of the trusted homodyne detector, with Gaussian modulation,
        in the asymptotic scenario.

        Args:
            Va (float): Alice's variance of modulation (in SNU).
            T (float): transmittance of the channel.
            xi (float): excess noise of the channel (in SNU).
            eta (float): efficiency of the detector.
            Vel (float): electronic noise of the detector (in SNU).

        Returns:
            float: Holevo's bound on the information between Eve and Bob in bits per symbol.
        """
        V = Va + 1
        chi_line = 1 / T - 1 + xi
        chi_hom = (1 + Vel) / eta - 1
        chi_tot = chi_line + chi_hom / T
        A = V**2 * (1 - 2 * T) + 2 * T + T**2 * (V + chi_line) ** 2
        B = T**2 * (V * chi_line + 1) ** 2
        C = (V * B**0.5 + T * (V + chi_line) + A * chi_hom) / (T * (V + chi_tot))
        D = B**0.5 * (V + B**0.5 * chi_hom) / (T * (V + chi_tot))
        nu_1 = (0.5 * (A + (A**2 - 4 * B) ** 0.5)) ** 0.5
        nu_2 = (0.5 * (A - (A**2 - 4 * B) ** 0.5)) ** 0.5
        nu_3 = (0.5 * (C + (C**2 - 4 * D) ** 0.5)) ** 0.5
        nu_4 = (0.5 * (C - (C**2 - 4 * D) ** 0.5)) ** 0.5
        return (
            g((nu_1 - 1) / 2)
            + g((nu_2 - 1) / 2)
            - g((nu_3 - 1) / 2)
            - g((nu_4 - 1) / 2)
        )
