from Mechanism.Constraints import *

# ==================Mapping=================#
def sensitivity_Cp_fun(ep, k, m, y, index):
    L = LValue(ep, k, m, y, index)
    if (index == 1) or (index == 4):
        retVal = k * m * (2 * L - m)
        return retVal
    if (index == 2) or (index == 5):
        retVal = 2 * k * m * (2 * L - m) / np.pi
        return retVal
    if (index == 3) or (index == 6):
        retVal = k * m * (2 * L - m) / 2
        return retVal


def mapping_fromRealToL(input_value, sensitivity_f, lower, ep, k, m, y, index):
    L = LValue(ep, k, m, y, index)
    sensitivity_Cp = sensitivity_Cp_fun(ep, k, m, y, index)
    C = sensitivity_Cp / sensitivity_f
    mapped_value = (input_value - lower) * C - L

    return mapped_value


def mapping_inverse_fromLToReal(input_value, sensitivity_f, lower, ep, k, m, y, index):
    L = LValue(ep, k, m, y, index)
    sensitivity_Cp = sensitivity_Cp_fun(ep, k, m, y, index)
    C = sensitivity_Cp / sensitivity_f
    mapped_inverse_value = (input_value + L) / C + lower

    return mapped_inverse_value


def listmapping_inverse_fromLToReal(input_list, sensitivity_f, lower, ep, k, m, y, index):
    mapped_inverse_list = []
    for i in range(len(input_list)):
        tmp = mapping_inverse_fromLToReal(input_list[i], sensitivity_f, lower, ep, k, m, y, index)
        mapped_inverse_list.append(tmp)
    return mapped_inverse_list


# ==========================================#