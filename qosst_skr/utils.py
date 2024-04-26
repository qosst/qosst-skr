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
Utils function for the computations of SKR.
"""
from math import log2


# pylint: disable=invalid-name
def g(value: float) -> float:
    """Useful function to compute the SKR, which is defined to be

    g(x) = (x+1)log(x+1) - xlog(x)

    with g vanishing when x vanish.

    Args:
        value (float): input.

    Returns:
        float: output.
    """
    if value == 0:
        return 0
    return (value + 1) * log2(value + 1) - value * log2(value)
