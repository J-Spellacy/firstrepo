import numpy as np
import matplotlib.pyplot as plt

# change this to be noisy data with a linear pattern
X = np.random.randint(0, 100, 100)
Y = np.random.randint(0, 100, 100)
X.sort()
Y.sort()

print(X)

def K_neighbor(y, Y, k=10):
    if y < round(k/2):
        Y_sample = Y[0:k]
    elif y+round(k/2) > len(Y):
        Y_sample = Y[-k:]
    else:
        Y_sample = Y[y-(round(k/2)):y+(round(k/2))]
    # print(f'{x}  {X[x]}')
    # print(X_sample)
    
    return(Y_sample)
    

# estimates the linear line equation  y = mx + c
def linear_reg(X, Y):
    # print(len(X))
    # print(range(len(X)))
    Y_expected = np.zeros_like(X)
    for i in range(len(X)):
        # print(i)
        # print(j)
        Y_expected[i] = np.mean(K_neighbor(i, Y))
        
    return Y_expected


Y_expected = linear_reg(X, Y)

# create a scatter plot of X and Y and then add line graph of  linear_reg(X, Y)
plt.figure(figsize=(10, 6))
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Scatter Plot and Linear Regression Line')

# Add a scatter plot
plt.scatter(X, Y, color='blue', label='Data Points')

# Add a line graph with the same x but different y values
plt.plot(X, Y_expected, color='red', label='Linear Regression Line')
# Add a legend
plt.legend()

# Show the plot
plt.show()
