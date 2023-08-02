import random
from Mechanism.Parameter_Optimization import *
import numpy as np

def PDF_fun(x, ep, k, m, y, Cp, index):
    L = LValue(ep, k, m, y, index)
    a = aValue(ep, k, m, y, Cp, index)
    t = (y + k) / np.e ** ep

    if (index == 1):
        P = 0
        if (x >= -L) and (x < a):
            P = y
        if (x >= a) and (x < a + m):
            P = y + k
        if (x >= a + m) and (x <= L):
            P = y
        return float3f(P)

    if (index == 2):
        P = 0
        if (x >= -L) and (x < a):
            P = y
        if (x >= a) and (x < a + m):
            P = y + k * sin(np.pi / m * (x - a))
        if (x >= a + m) and (x <= L):
            P = y
        return float3f(P)

    if (index == 3):
        P = 0
        if (x >= -L) and (x < a):
            P = y
        if (x >= a) and (x < a + m / 2):
            P = y + 2 * k / m * x - 2 * a * k / m
        if (x >= a + m / 2) and (x < a + m):
            P = y - 2 * k / m * x + 2 * (a + m) * k / m
        if (x >= a + m) and (x <= L):
            P = y
        return float3f(P)

    if (index == 4):
        P = 0
        if (x >= -L) and (x < a):
            P = -(y - t) / L ** 4 * x ** 4 + y
        if (x >= a) and (x < a + m):
            P = -(y - t) / L ** 4 * x ** 4 + y + k
        if (x >= a + m) and (x <= L):
            P = -(y - t) / L ** 4 * x ** 4 + y
        return float3f(P)

    if (index == 5):
        P = 0
        if (x >= -L) and (x < a):
            P = -(y - t) / L ** 4 * x ** 4 + y
        if (x >= a) and (x < a + m):
            P = -(y - t) / L ** 4 * x ** 4 + y + k * sin(np.pi / m * (x - a))
        if (x >= a + m) and (x <= L):
            P = -(y - t) / L ** 4 * x ** 4 + y
        return float3f(P)

    if (index == 6):
        P = 0
        if (x >= -L) and (x < a):
            P = -(y - t) / L ** 4 * x ** 4 + y
        if (x >= a) and (x < a + m / 2):
            P = -(y - t) / L ** 4 * x ** 4 + y + 2 * k / m * x - 2 * a * k / m
        if (x >= a + m / 2) and (x < a + m):
            P = -(y - t) / L ** 4 * x ** 4 + y - 2 * k / m * x + 2 * (a + m) * k / m
        if (x >= a + m) and (x <= L):
            P = -(y - t) / L ** 4 * x ** 4 + y
        return float3f(P)


def generate_perturbed_list(ep, k, m, y, Cp, index):
    L = LValue(ep, k, m, y, index)
    a = aValue(ep, k, m, y, Cp, index)
    t = (y + k) / np.e ** ep

    divid = 10000
    step = 2 * L / divid
    x_count = -L
    X_axis = []
    P_axis = []
    Perturbed_list = []

    while (x_count <= L):
        P_x = PDF_fun(x_count, ep, k, m, y, Cp, index)
        P_axis.append(P_x)
        X_axis.append(x_count)
        x_count = x_count + step

    for i in range(len(X_axis)):
        rp = P_axis[i]
        rp = int(rp * 1000)
        for j in range(rp):
            Perturbed_list.append(X_axis[i])

    random.shuffle(Perturbed_list)
    return Perturbed_list

def perturbation_fun_oneCall(ep, fd, sensitivity, lower, k, m, y, index):
    Cp = mapping_fromRealToL(fd, sensitivity, lower, ep, k, m, y, index)
    if (checkConstraints(ep, k, m, y, Cp, index) != 0):
        print("Constraints errors")
        return 0
    O_perturbed = generate_perturbed_list(ep, k, m, y, Cp, index)
    Out_perturbed = listmapping_inverse_fromLToReal(O_perturbed, sensitivity, lower, ep, k, m, y, index)

    return Out_perturbed[0]


def perturbation_fun_multipleCall(ep, fd, sensitivity, lower, k, m, y, index, repeat_times):
    Cp = mapping_fromRealToL(fd, sensitivity, lower, ep, k, m, y, index)
    if (checkConstraints(ep, k, m, y, Cp, index) != 0):
        print("Constraints errors")
        return 0
    O_perturbed = generate_perturbed_list(ep, k, m, y, Cp, index)
    Out_perturbed = listmapping_inverse_fromLToReal(O_perturbed, sensitivity, lower, ep, k, m, y, index)

    retVal = []
    for i in range(repeat_times):
        retVal.append(Out_perturbed[i])

    return retVal


def perturbation_fun_optimized_oneCall(ep, fd, sensitivity, lower, index):
    k_best, m_best, y_best = parameter_optimization(ep, index)
    Cp = mapping_fromRealToL(fd, sensitivity, lower, ep, k_best, m_best, y_best, index)
    O_perturbed = generate_perturbed_list(ep, k_best, m_best, y_best, Cp, index)
    Out_perturbed = listmapping_inverse_fromLToReal(O_perturbed, sensitivity, lower, ep, k_best, m_best, y_best, index)

    return Out_perturbed[0]


def perturbation_fun_optimized_multipleCall(ep, fd, sensitivity, lower, index, repeat_times):
    k_best, m_best, y_best = parameter_optimization(ep, index)
    Cp = mapping_fromRealToL(fd, sensitivity, lower, ep, k_best, m_best, y_best, index)
    O_perturbed = generate_perturbed_list(ep, k_best, m_best, y_best, Cp, index)
    Out_perturbed = listmapping_inverse_fromLToReal(O_perturbed, sensitivity, lower, ep, k_best, m_best, y_best, index)

    retVal = []
    for i in range(repeat_times):
        retVal.append(Out_perturbed[i])

    return retVal

def perturbation_fun_Var_and_HRate(fd, sensitivity, lower, ep, k, m, y, index, repeat_times):
    Cp = mapping_fromRealToL(fd, sensitivity, lower, ep, k, m, y, index)

    if (checkConstraints(ep, k, m, y, Cp, index) != 0):
        print("Constraints errors")
        return 0

    H1 = H1Rate(ep, k, m, y, index)
    H2 = H2Rate(Cp, ep, k, m, y, index)

    O_perturbed = generate_perturbed_list(ep, k, m, y, Cp, index)
    Out_perturbed = listmapping_inverse_fromLToReal(O_perturbed, sensitivity, lower, ep, k, m, y, index)
    retVal = []
    for i in range(repeat_times):
        retVal.append(Out_perturbed[i])

    MSE = calMSE_CompDP(retVal, fd)
    return MSE, H1, H2

def calMSE_CompDP(input_list, fd):
    MSE = 0
    for i in range(len(input_list)):
        MSE = MSE + (input_list[i] - fd) ** 2
    MSE = MSE / len(input_list)

    return (MSE)


def calRE_CompDP(input_list, fd):
    RE = 0
    for i in range(len(input_list)):
        RE = RE + abs(input_list[i] - fd)
    RE = RE / len(input_list)

    return (RE)

def calAL_CompDP(input_list, fd):
    AL = []
    for i in range(len(input_list)):
        tmp_al = abs((input_list[i]-fd)/fd)
        AL.append(tmp_al)

    return AL

def perturbation_fun_MSE(ep, fd, sensitivity, lower, index, repeat_times):
    perturbed_list = perturbation_fun_optimized_multipleCall(ep, fd, sensitivity, lower, index, repeat_times)
    MSE = calMSE_CompDP(perturbed_list, fd)

    return MSE

def perturbation_fun_RE(ep, fd, sensitivity, lower, index, repeat_times):
    perturbed_list = perturbation_fun_optimized_multipleCall(ep, fd, sensitivity, lower, index, repeat_times)
    RE = calRE_CompDP(perturbed_list, fd)

    return RE

def perturbation_fun_MSE_RE(ep, fd, sensitivity, lower, index, repeat_times):
    perturbed_list = perturbation_fun_optimized_multipleCall(ep, fd, sensitivity, lower, index, repeat_times)
    MSE = calMSE_CompDP(perturbed_list, fd)
    RE = calRE_CompDP(perturbed_list, fd)

    return MSE, RE

def perturbation_fun_AL(ep, fd, sensitivity, lower, index, repeat_times):
    perturbed_list = perturbation_fun_optimized_multipleCall(ep, fd, sensitivity, lower, index, repeat_times)
    AL = calAL_CompDP(perturbed_list, fd)
    return AL