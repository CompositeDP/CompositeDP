import math
import numpy as np

def float3f(num):
    return float(format(num, '.3f'))


def float2f(num):
    return float(format(num, '.2f'))


# ==============Constraints=================#
def LValue(ep, k, m, y, index):
    _LValue = -1
    t = (y + k) / np.e ** ep

    if (index == 1):
        _LValue = (1 - k * m) / (2 * y)

    if (index == 2):
        _LValue = (-k * m + np.pi / 2) / (np.pi * y)

    if (index == 3):
        _LValue = (-k * m + 2) / (4 * y)

    if (index == 4):
        _LValue = -5 * (k * m - 1) / (2 * (t + 4 * y))

    if (index == 5):
        _LValue = -5 * (2 * k * m - np.pi) / (2 * np.pi * (t + 4 * y))

    if (index == 6):
        _LValue = -5 * (k * m - 2) / (4 * (t + 4 * y))

    return _LValue


def aValue(ep, k, m, y, Cp, index):
    if ((index == 1) or (index == 4)):
        _aValue = (2 * Cp - k * m ** 2) / (2 * k * m)
        return _aValue

    if ((index == 2) or (index == 5)):
        _aValue = (np.pi * Cp - k * m ** 2) / (2 * k * m)
        return _aValue

    if ((index == 3) or (index == 6)):
        _aValue = (4 * Cp - k * m ** 2) / (2 * k * m)
        return _aValue


def checkConstraints(ep, k, m, y, Cp, index):
    if k <= 0:
        return -1
    if m <= 0:
        return -2
    if y <= 0:
        return -3

    L = LValue(ep, k, m, y, index)
    a = aValue(ep, k, m, y, Cp, index)
    t = (y + k) / np.e ** ep

    if (index == 1):
        if k * m >= 1:
            return -4
        if (Cp > k * m * (2 * L - m) / 2) or (Cp < -k * m * (2 * L - m) / 2):
            return -5
        if k > 1 - y:
            return -6
        if k > y * (np.e ** ep - 1):
            return -7

    if (index == 2):
        if 2 * k * m / np.pi >= 1:
            return -4
        if (Cp > k * m * (2 * L - m) / np.pi) or (Cp < -k * m * (2 * L - m) / np.pi):
            return -5
        if k > 1 - y:
            return -6
        if k >= y * (np.e ** ep - 1):
            return -7

    if (index == 3):
        if k * m / 2 >= 1:
            return -4
        if (Cp > k * m * (2 * L - m) / 4) or (Cp < -k * m * (2 * L - m) / 4):
            return -5
        if k > 1 - y:
            return -6
        if k > y * (np.e ** ep - 1):
            return -7

    if (index == 4):
        if k * m >= 1:
            return -4
        if (Cp > k * m * (2 * L - m) / 2) or (Cp < -k * m * (2 * L - m) / 2):
            return -5
        if k > 1 - y:
            return -6
        if t >= y:
            return -7

    if (index == 5):
        if 2 * k * m / np.pi >= 1:
            return -4
        if (Cp > k * m * (2 * L - m) / np.pi) or (Cp < -k * m * (2 * L - m) / np.pi):
            return -5
        if k > 1 - y:
            return -6
        if t >= y:
            return -7

    if (index == 6):
        if k * m / 2 >= 1:
            return -4
        if (Cp > k * m * (2 * L - m) / 4) or (Cp < -k * m * (2 * L - m) / 4):
            return -5
        if k > 1 - y:
            return -6
        if t >= y:
            return -7

    return 0

# ==========================================#