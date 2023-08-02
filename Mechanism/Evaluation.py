from Mechanism.Constraints import *

def reduceRate(var1, var2):
    rate = (var1 - var2) / var1
    return float(rate)

def H1Rate(ep, k, m, y, index):
    L = LValue(ep, k, m, y, index)
    t = (y + k) / np.e ** ep
    if (index == 1):
        S1 = k*m
        S2 = 2*L*y
        return float(S2 / S1)
    if (index == 2):
        S1 = 2*k*m/np.pi
        S2 = 2 * L * y
        return float(S2 / S1)
    if (index == 3):
        S1 = k*m/2
        S2 = 2 * L * y
        return float(S2 / S1)
    if (index == 4):
        S1 = k*m
        S2 = 2 * L * (t - y) / 5 + 2 * L * y
        return float(S2 / S1)
    if (index == 5):
        S1 = 2*k*m/np.pi
        S2 = 2 * L * (t - y) / 5 + 2 * L * y
        return float(S2 / S1)
    if (index == 6):
        S1 = k*m/2
        S2 = 2 * L * (t - y) / 5 + 2 * L * y
        return float(S2 / S1)

def H2Rate(Cp, ep, k, m, y, index):
    L = LValue(ep, k, m, y, index)
    t = (y + k) / np.e ** ep
    if (index == 1) or (index == 2) or (index ==3):
        H2 = 0.33333
        return H2
    if (index == 4) or (index == 5) or (index ==6):
        if Cp>=0:
            H2 = (Cp**5*(t - y) + 1.25*L**4*y*(Cp + L) + 0.2373046875*(Cp - 0.333333333333333*L)**5*(-t + y))/(Cp**5*(t - y) + 3.75*L**4*y*(Cp + L) - 0.2373046875*(0.333333333333333*Cp - L)**5*(t - y))
        else:
            H2 = (Cp**5*(t - y) + 1.25*L**4*y*(Cp - L) + 0.2373046875*(Cp + 0.333333333333333*L)**5*(-t + y))/(Cp**5*(t - y) + 3.75*L**4*y*(Cp - L) - 0.2373046875*(0.333333333333333*Cp + L)**5*(t - y))
        return H2


def theory_var_fun(ep, k, m, y, Cp_assume, index):
    Cp = Cp_assume
    L = LValue(ep, k, m, y, index)
    a = aValue(ep, k, m, y, Cp, index)
    t = (y + k) / np.e ** ep

    if (index == 1):
        variance = -Cp ** 2 + 2 * L ** 3 * y / 3 + a ** 2 * k * m + a * k * m ** 2 + k * m ** 3 / 3
        return float(variance)

    if (index == 2):
        variance = -Cp ** 2 + 2 * L ** 3 * y / 3 + a ** 2 * k * m / pi - 4 * k * m ** 3 / pi ** 3 + k * m * (
                    a + m) ** 2 / pi
        return float(variance)

    if (index == 3):
        variance = -Cp ** 2 + 2 * L ** 3 * y / 3 + a ** 2 * k * m / 2 + a * k * m ** 2 / 2 + 7 * k * m ** 3 / 48
        return float(variance)

    if (index == 4):
        variance = -Cp ** 2 + 2 * L ** 3 * t / 7 + 8 * L ** 3 * y / 21 + a ** 2 * k * m + a * k * m ** 2 + k * m ** 3 / 3
        return float(variance)

    if (index == 5):
        variance = -Cp ** 2 + 2 * L ** 3 * t / 7 + 8 * L ** 3 * y / 21 + 2 * a ** 2 * k * m / pi + 2 * a * k * m ** 2 / pi - 4 * k * m ** 3 / pi ** 3 + k * m ** 3 / pi
        return float(variance)

    if (index == 6):
        variance = -Cp ** 2 + 2 * L ** 3 * t / 7 + 8 * L ** 3 * y / 21 + a ** 2 * k * m / 2 + a * k * m ** 2 / 2 + 7 * k * m ** 3 / 48
        return float(variance)

    print("Index errors")
    return -2