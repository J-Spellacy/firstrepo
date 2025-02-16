import numpy as np
import matplotlib.pyplot as plt


X = np.random.randint(0, 100, 100)
Y = np.random.randint(0, 100, 100)

print(X)

def K_neighbor(x, X, k=10):
    if x < round(k/2):
        X_sample = X[0:k]
    elif x+round(k/2) > len(X):
        X_sample = X[-k:]
    else:
        X_sample = X[x-(round(k/2)):x+(round(k/2))]
    # print(f'{x}  {X[x]}')
    # print(X_sample)
    
    return(X_sample)
    

# estimates the linear line equation  y = mx + c
def linear_reg(X, Y):
    # print(len(X))
    # print(range(len(X)))
    Y_hat = np.zeros_like(X)
    for i in range(len(X)):
        # print(i)
        # print(j)
        Y_hat[i] = np.mean(K_neighbor(i, X))
        
    return Y_hat


print(linear_reg(X, Y))

# create a scatter plot of X and Y and then add line graph of  linear_reg(X, Y)

