import numpy as np
from numbers import Real
import discretegauss
import cdp2adp

def Laplace_fun(sensitivity, epsilon):
    noise = np.random.laplace(0, sensitivity / epsilon)
    return noise


def Gaussian_fun(sensitivity, epsilon):
    delta = 1e-6
    sigma = np.sqrt(2 * np.log(1.25 / delta)) * sensitivity / epsilon
    noise = np.random.normal(loc=0, scale=sigma)
    return noise


def Laplace_discrete_fun(sensitivity, epsilon):
    scale = sensitivity / epsilon
    noise = discretegauss.sample_dlaplace(scale)
    return noise


def Gaussian_discrete_fun(sensitivity, epsilon):
    delta = 1e-6
    sigma = np.sqrt(2 * np.log(1.25 / delta)) * sensitivity / epsilon
    variance = discretegauss.variance(sigma ** 2)
    noise = variance ** 0.5
    return noise


def _truncate(value, lower, upper):
    if value > upper:
        return upper
    if value < lower:
        return lower

    return value


def _laplace_sampler(unif1, unif2, unif3, unif4):
    return np.log(1 - unif1) * np.cos(np.pi * unif2) + np.log(1 - unif3) * np.cos(np.pi * unif4)


def check_sensitivity(sensitivity):
    if not isinstance(sensitivity, Real):
        raise TypeError("Sensitivity must be numeric")

    if sensitivity < 0:
        raise ValueError("Sensitivity must be non-negative")

    return float(sensitivity)


def check_epsilon_delta(epsilon, delta):
    if not isinstance(epsilon, Real) or not isinstance(delta, Real):
        raise TypeError("Epsilon and delta must be numeric")

    if epsilon < 0:
        raise ValueError("Epsilon must be non-negative")

    if not 0 <= delta <= 1:
        raise ValueError("Delta must be in [0, 1]")

    if epsilon + delta == 0:
        raise ValueError("Epsilon and Delta cannot both be zero")

    return float(epsilon), float(delta)


def Laplace_truncated_fun(value, epsilon, delta, sensitivity, lower, upper):
    # perform all the checks
    rng = np.random.RandomState()

    epsilon, delta = check_epsilon_delta(epsilon, delta)
    sensitivity = check_sensitivity(sensitivity)

    if not isinstance(value, Real):
        raise TypeError("Value to be randomised must be a number")

    scale = sensitivity / (epsilon - np.log(1 - delta))
    standard_laplace = _laplace_sampler(rng.random(), rng.random(), rng.random(), rng.random())

    noisy_value = value - scale * standard_laplace
    # truncate the noisy value
    return _truncate(noisy_value, lower, upper)


def Laplace_truncated_variance_fun(value, epsilon, delta, sensitivity, lower, upper):
    # perform all the checks
    epsilon, delta = check_epsilon_delta(epsilon, delta)
    sensitivity = check_sensitivity(sensitivity)

    if not isinstance(value, Real):
        raise TypeError("Value to be randomised must be a number")

    shape = sensitivity / epsilon

    variance = value ** 2 + shape * (lower * np.exp((lower - value) / shape) - upper * np.exp((value - upper) / shape))
    variance += (shape ** 2) * (2 - np.exp((lower - value) / shape) - np.exp((value - upper) / shape))

    bias = shape / 2 * (np.exp((lower - value) / shape) - np.exp((value - upper) / shape))
    variance -= (bias + value) ** 2

    return variance


def Laplace_truncated_discrete_fun(value, epsilon, delta, sensitivity, lower, upper):
    perturbed = Laplace_truncated_fun(value, epsilon, delta, sensitivity, lower, upper)
    noise = perturbed - value
    return round(noise)


def Laplace_MSE(sensitivity, epsilon, repeat_times):
    MSE = 0
    for i in range(repeat_times):
        tmp = Laplace_fun(sensitivity, epsilon)
        MSE = MSE + tmp ** 2

    MSE = MSE / repeat_times
    return MSE


def Laplace_discrete_MSE(sensitivity, epsilon, repeat_times):
    MSE = 0
    for i in range(repeat_times):
        tmp = Laplace_discrete_fun(sensitivity, epsilon)
        MSE = MSE + tmp ** 2

    MSE = MSE / repeat_times
    return MSE


def Laplace_truncated_discrete_MSE(value, sensitivity, epsilon, delta, lower, upper, repeat_times):
    MSE = 0
    for i in range(repeat_times):
        tmp = Laplace_truncated_discrete_fun(value, epsilon, delta, sensitivity, lower, upper)
        MSE = MSE + tmp ** 2

    MSE = MSE / repeat_times
    return MSE


def Gaussian_MSE(sensitivity, epsilon, repeat_times):
    MSE = 0
    for i in range(repeat_times):
        tmp = Gaussian_fun(sensitivity, epsilon)
        MSE = MSE + tmp ** 2

    MSE = MSE / repeat_times
    return MSE


def Gaussian_discrete_MSE(sensitivity, epsilon, repeat_times):
    MSE = 0
    for i in range(repeat_times):
        tmp = Gaussian_discrete_fun(sensitivity, epsilon)
        MSE = MSE + tmp ** 2

    MSE = MSE / repeat_times
    return MSE


def Laplace_MSE_Log(sensitivity, epsilon, repeat_times, d):
    MSE = 0
    for i in range(repeat_times):
        tmp = Laplace_fun(sensitivity, epsilon)
        MSE = MSE + tmp ** 2

    MSE = MSE / repeat_times
    return np.log(MSE + d)


def Laplace_discrete_MSE_Log(sensitivity, epsilon, repeat_times, d):
    MSE = 0
    for i in range(repeat_times):
        tmp = Laplace_discrete_fun(sensitivity, epsilon)
        MSE = MSE + tmp ** 2

    MSE = MSE / repeat_times
    return np.log(MSE + d)


def Laplace_truncated_discrete_MSE_Log(value, sensitivity, epsilon, delta, lower, upper, repeat_times, d):
    MSE = 0
    for i in range(repeat_times):
        tmp = Laplace_truncated_discrete_fun(value, epsilon, delta, sensitivity, lower, upper)
        MSE = MSE + tmp ** 2

    MSE = MSE / repeat_times
    return np.log(MSE + d)


def Gaussian_MSE_Log(sensitivity, epsilon, repeat_times, d):
    MSE = 0
    for i in range(repeat_times):
        tmp = Gaussian_fun(sensitivity, epsilon)
        MSE = MSE + tmp ** 2

    MSE = MSE / repeat_times
    return np.log(MSE + d)


def Gaussian_discrete_MSE_Log(sensitivity, epsilon, repeat_times, d):
    MSE = 0
    for i in range(repeat_times):
        tmp = Gaussian_discrete_fun(sensitivity, epsilon)
        MSE = MSE + tmp ** 2

    MSE = MSE / repeat_times
    return np.log(MSE + d)


def Laplace_RE(sensitivity, epsilon, repeat_times):
    RE = 0
    for i in range(repeat_times):
        tmp = Laplace_fun(sensitivity, epsilon)
        RE = RE + abs(tmp)

    RE = RE / repeat_times
    return RE


def Laplace_discrete_RE(sensitivity, epsilon, repeat_times):
    RE = 0
    for i in range(repeat_times):
        tmp = Laplace_discrete_fun(sensitivity, epsilon)
        RE = RE + abs(tmp)

    RE = RE / repeat_times
    return RE


def Laplace_truncated_discrete_RE(value, sensitivity, epsilon, delta, lower, upper, repeat_times):
    RE = 0
    for i in range(repeat_times):
        tmp = Laplace_truncated_discrete_fun(value, epsilon, delta, sensitivity, lower, upper)
        RE = RE + abs(tmp)

    RE = RE / repeat_times
    return RE


def Gaussian_RE(sensitivity, epsilon, repeat_times):
    RE = 0
    for i in range(repeat_times):
        tmp = Gaussian_fun(sensitivity, epsilon)
        RE = RE + abs(tmp)

    RE = RE / repeat_times
    return RE


def Gaussian_discrete_RE(sensitivity, epsilon, repeat_times):
    RE = 0
    for i in range(repeat_times):
        tmp = Gaussian_discrete_fun(sensitivity, epsilon)
        RE = RE + abs(tmp)

    RE = RE / repeat_times
    return RE


