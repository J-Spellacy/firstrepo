import numpy as np
import matplotlib.pyplot as plt



# Define the grid
x = np.linspace(-5, 5, 20)
y = np.linspace(-5, 5, 20)
z = np.linspace(-5, 5, 20)

# Define the grid
x = np.linspace(-5, 5, 10)
y = np.linspace(-5, 5, 10)
z = np.linspace(-5, 5, 10)
X, Y, Z = np.meshgrid(x, y, z)

# Define the vector field components
U = X
V = -Y
W = Z


def twod_vector_field(X, Y, U, V):
    # Plot the vector field
    plt.figure()
    plt.quiver(X, Y, U, V)
    plt.title('Vector Field')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid()

    # Mark the origin with a point labeled 'O'
    plt.scatter(0, 0, color='black', s=20, marker='x')
    plt.text(0, 0, 'O', fontsize=12, ha='right')

    plt.show()


def threed_vector_field(X, Y, Z, U, V, W):
    # Plot the vector field
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(X, Y, Z, U, V, W, length=0.5, linewidth=0.5)

    # Mark the origin with a point labeled 'O'
    ax.scatter(0, 0, 0, color='black', s=100, marker='o')
    ax.text(0, 0, 0, 'O', fontsize=12, ha='right')

    ax.set_title('3D Vector Field')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    plt.show() 

threed_vector_field(X, Y, Z, U, V, W)
# twod_vector_field(X, Y, U, V)