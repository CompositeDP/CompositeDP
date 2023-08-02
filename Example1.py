from Perturbation_Mechanism import *
#from Traditional_Mechanism import *

# Examples:
# A age dataset about teenagers= {1,5,10,20,30}
# Maximum query f(D) = 30, f'(D) = 20

fd = 30
sensitivity = 10
lower_bound = 0
epsilon = 1
index = 3

k = 0.5
m = 0.4
y = 0.3
index = 1
repeat_times = 1000


# Example-1:
print("Example-1:")
# To conduct perturbation via the parameters listed above:

# For one call, the final perturbed result is as follows:
Op = perturbation_fun_oneCall(epsilon, fd, sensitivity, lower_bound, k, m, y, index)
print("Op = ", Op)

# For multiple call, the final perturbed results are as follows (repeat 1000 times):
Op_Multiple = perturbation_fun_multipleCall(epsilon, fd, sensitivity, lower_bound, k, m, y, index, repeat_times)
print("Op_Multiple =", Op_Multiple)

# Example-2:
print("Example-2:")
# To conduct perturbation via the parameter optimization algorithm:

# For one call, the final perturbed result is as follows:
Op = perturbation_fun_optimized_oneCall(epsilon, fd, sensitivity, lower_bound, index)
print("Op = ", Op)

# For multiple call, the final perturbed results are as follows (repeat 1000 times):
Op_Multiple = perturbation_fun_optimized_multipleCall(epsilon, fd, sensitivity, lower_bound, index, repeat_times)
print("Op_Multiple =", Op_Multiple)

# Example-3:
print("Example-3:")
# To Work out Variance, R1, R2 via the parameters listed above:
MSE, R1, R2 = perturbation_fun_Var_and_HRate(fd, sensitivity,lower_bound, epsilon,k,m,y,index,repeat_times)

print("MSE =", MSE)
print("R1 =", R1)
print("R2 =", R2)

