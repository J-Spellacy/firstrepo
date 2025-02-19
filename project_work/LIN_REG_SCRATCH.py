import numpy as np
import matplotlib.pyplot as plt

def K_neighbor(y, Y, k=10):
    if y < round(k/2):
        Y_sample = Y[0:k]
    elif y+round(k/2) > len(Y):
        Y_sample = Y[-k:]
    else:
        Y_sample = Y[y-(round(k/2)):y+(round(k/2))]
    # print(f'{x}  {X[x]}')
    # print(X_sample)
    
    return Y_sample
    

# estimates the linear line equation  y = mx + c
def expected_val_func(X, Y, k):
    # print(len(X))
    # print(range(len(X)))
    Y_expected = np.zeros_like(X)
    for i in range(len(X)):
        # print(i)
        # print(j)
        Y_expected[i] = np.mean(K_neighbor(i, Y, k))
        
    return Y_expected, k




def plot_overlayed(X, Y, Y_expected, Y_hat, k):
    # create a scatter plot of X and Y and then add line graph of expected_val_func(X, Y)
    plt.figure(figsize=(10, 6))
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot and Linear Regression Line')

    # Add a scatter plot
    plt.scatter(X, Y, color='blue', label='Data Points')

    # Add a line graph with the same x but different y values
    plt.plot(X, Y_hat, color='red', label='Linear Regression Line')
    plt.plot(X, Y_expected, color='red', label=f'K-nearest-neighbor Regression Line k={k}')
    # Add a legend
    plt.legend()

    # Show the plot
    plt.show()

'''
estimates a function Y_hat = beta_hat_0 + beta_hat_1*X which is an estimate of Y = beta_0 + beta_1*X + epsilon (intercept, slope, error)
assuming the original data is of the form above, estimates these parameters by minimizing the sum of squared residuals or squared errors
from RSS = sum_i = 1 to n (Y_i - beta_hat_0 - beta_hat_1*X_i)^2 where n is the number of data points
it can be shown with calculus that the optimal beta_0 and beta_1 are given by:
beta_hat_1 = sum_i = 1 to n (X_i - X_bar)(Y_i - Y_bar) / sum_i = 1 to n (X_i - X_bar)^2
beta_hat_0 = y_bar - beta_hat_1*X_bar
'''
def linear_regression(X, Y):
    Kn_res_sum_sq = 0
    Y_expected, k = expected_val_func(X, Y, k=10)
    x_bar, y_bar = np.mean(X), np.mean(Y)
    B1_numerator, B1_denominator = 0, 0
    for i in range(len(X)):
        Kn_res_sum_sq += (Y[i] - Y_expected[i])**2
        B1_numerator  += (X[i] - x_bar)*(Y[i] - y_bar)
        B1_denominator += (X[i] - x_bar)**2
    print(f'K-nearest-neighbor Residual Sum of Squares: {Kn_res_sum_sq}')
    beta_hat_1 = B1_numerator / B1_denominator
    beta_hat_0 = y_bar - beta_hat_1*x_bar
    Y_hat = beta_hat_0 + beta_hat_1*X
    res_sum_sq = 0
    for i in range(len(X)):
        res_sum_sq += (Y[i] - Y_hat[i])**2
    print(f'Final Residual Sum of Squares: {res_sum_sq}')
    return Y_hat, beta_hat_0, beta_hat_1


# along with 3d plot in main plots the RSS for different beta_0 and beta_1 values like in ISLP textbook
def beta_estimate_demonstration(X, Y, num_points = 100):
    beta_1_estimates = np.linspace(start = -100, stop = 100, num = num_points, endpoint = True)
    beta_0_estimates = np.linspace(start = -100, stop = 100, num = num_points, endpoint = True)
    RSS = np.zeros((100, 100))
    Y_hat = np.zeros_like(beta_0_estimates)
    for i in range(num_points):
        for j in range(num_points):
            Y_hat = beta_0_estimates[j] + beta_1_estimates[i]*X
            RSS[i, j] += np.sum((Y-Y_hat)**2)
 
    beta_grid = np.meshgrid(beta_0_estimates, beta_1_estimates)
    return RSS, beta_grid

if __name__ == '__main__':
    # change this to be noisy data with a linear pattern
    X = np.random.randint(0, 100, 100)
    Y = np.random.randint(0, 100, 100)
    X.sort()
    Y.sort()

    # print(X)
    # Y_expected, k = expected_val_func(X, Y, k=10)
    # # plot_overlayed(X, Y, Y_expected)
    Y_hat, beta_hat_1, beta_hat_0 = linear_regression(X, Y)
    # plot_overlayed(X, Y, Y_hat, Y_expected, k)
    # print(Y_hat)
    RSS, beta_grid = beta_estimate_demonstration(X, Y)
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(beta_grid[0], beta_grid[1], RSS, cmap='viridis')
    ax.scatter(beta_hat_0, beta_hat_1, 0, color='red')
    ax.set_xlabel('Beta_0')
    ax.set_ylabel('Beta_1')
    ax.set_zlabel('RSS')
    plt.show()