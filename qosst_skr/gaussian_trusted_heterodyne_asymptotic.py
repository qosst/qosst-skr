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
Calulator for Gaussian Modulation with Trusted detector and Heterodyne detection using the asymptotic regime.
"""
from math import log2

from qosst_core.skr_computations import BaseCVQKDSKRCalculator

from qosst_skr.utils import g


# pylint: disable=invalid-name, too-few-public-methods
class GaussianTrustedHeterodyneAsymptotic(BaseCVQKDSKRCalculator):
    """
    This assumes:

    * Gaussian Modulation
    * Trusted detector
    * Heterodyne Detection
    * Asymptotic key rate

    S Fossier, E Diamanti, T Debuisschert, R Tualle-Brouri, & P Grangier (2009). Improvement of continuous-variable quantum key distribution systems by using optical preamplifiers. Journal of Physics B: Atomic, Molecular and Optical Physics, 42(11), 114014.
    """

    # pylint: disable=too-many-arguments
    @staticmethod
    def skr(**kwargs) -> float:
        """
        This method computes the secret key rate in the case of the trusted heterodyne detector, with Gaussian modulation,
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
        beta = kwargs.pop("beta", 0.95)
        return GaussianTrustedHeterodyneAsymptotic._skr(Va, T, xi, eta, Vel, beta)

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
        key_rate = GaussianTrustedHeterodyneAsymptotic._iab(
            Va, T, xi, eta, Vel, beta
        ) - GaussianTrustedHeterodyneAsymptotic._holevo_bound(Va, T, xi, eta, Vel)
        if key_rate > 0:
            return key_rate
        return 0.0

    @staticmethod
    def _iab(
        Va: float, T: float, xi: float, eta: float, Vel: float, beta: float
    ) -> float:
        """
        Compute the information shared by Alice and Bob in the case of the trusted heterodyne detector, with Gaussian modulation,
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
        chi_line = 1 / T - 1 + xi
        chi_het = (1 + (1 - eta) + 2 * Vel) / eta
        chi_tot = chi_line + chi_het / T
        return beta * log2((1 + Va + chi_tot) / (1 + chi_tot))

    # pylint: disable=too-many-locals
    @staticmethod
    def _holevo_bound(Va: float, T: float, xi: float, eta: float, Vel: float) -> float:
        """
        Compute the Holevo bound on the information between Bob and Eve in the case of the trusted heterodyne detector, with Gaussian modulation,
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
        chi_het = (1 + (1 - eta) + 2 * Vel) / eta
        chi_tot = chi_line + chi_het / T
        A = V**2 * (1 - 2 * T) + 2 * T + T**2 * (V + chi_line) ** 2
        B = T**2 * (V * chi_line + 1) ** 2
        C = (
            1
            / (T * (V + chi_tot)) ** 2
            * (
                A * chi_het**2
                + B
                + 1
                + 2 * chi_het * (V * B**0.5 + T * (V + chi_line))
                + 2 * T * (V**2 - 1)
            )
        )
        D = (V + B**0.5 * chi_het) ** 2 / (T * (V + chi_tot)) ** 2

        lambda_1 = (0.5 * (A + (A**2 - 4 * B) ** 0.5)) ** 0.5
        lambda_2 = (0.5 * (A - (A**2 - 4 * B) ** 0.5)) ** 0.5
        lambda_3 = (0.5 * (C + (C**2 - 4 * D) ** 0.5)) ** 0.5
        lambda_4 = (0.5 * (C - (C**2 - 4 * D) ** 0.5)) ** 0.5
        lambda_5 = 1

        return (
            g((lambda_1 - 1) / 2)
            + g((lambda_2 - 1) / 2)
            - g((lambda_3 - 1) / 2)
            - g((lambda_4 - 1) / 2)
            - g((lambda_5 - 1) / 2)
        )
