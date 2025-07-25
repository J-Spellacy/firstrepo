import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def mse(actual: np.ndarray, predicted: np.ndarray) -> float:
    return np.mean((actual - predicted) ** 2)

def relu(imput: np.ndarray) -> np.ndarray:
    return np.maximum(0, input)

def predict(input: np.ndarray, weights: np.ndarray, bias: np.ndarray) -> np.ndarray:
    return np.dot(input, weights) + bias

## create a function to generate batches to exhaust the datatset at each epoch
def generate_batches(X: np.ndarray, y: np.ndarray, batch_size: int) -> tuple:
    indices = np.random.permutation(len(y))
    X_shuffled, y_shuffled = X[indices], y[indices]
    for start in range(0, len(y), batch_size):
        end = start + batch_size
        yield X_shuffled[start:end], y_shuffled[start:end]
        
# currently batch function is ai mumbo jumbo, needs fixing

def batch_gradient_descent(learning_rate: float, batch_size: int, X: np.ndarray, y: np.ndarray, weights: np.ndarray, bias: np.ndarray, epochs: int) -> tuple:
    history = []
    for epoch in range(epochs):
        for batch_step in range(0, len(y), batch_size):
            indices = np.sort(np.random.choice(len(y), size=batch_size, replace=False))
            X_batch, y_batch = X[indices], y[indices]  # In a real scenario, you would select a batch here
            predictions = predict(input=X_batch, weights=weights, bias=bias)
            error = predictions - y_batch.reshape(-1, 1)

            # Calculate gradients (needs fixing)
            weight_gradients = (1/len(y_batch)) * np.dot(X_batch.T, error)
            bias_gradient = (1/len(y_batch)) * np.sum(error)

            weights -= learning_rate * weight_gradients
            bias -= learning_rate * bias_gradient
            current_error = mse(y_batch, predictions.flatten())
        print(f"Epoch {epoch+1}/{epochs}, Loss (MSE): {current_error}")
        history.append(current_error)

    return weights, bias, history

def generate_synthetic_data(num_samples: int, num_features: int, noise_level: float = 0.1) -> pd.DataFrame:
    # Set random seed for reproducibility
    np.random.seed(42)

    # Generate random features (uniform between -1 and 1, for example)
    x1 = np.random.uniform(-1, 1, size=num_samples)
    x2 = np.random.uniform(-1, 1, size=num_samples)

    # Compute the target with noise
    noise = np.random.normal(0, 0.1, size=num_samples)  # Gaussian noise with mean 0 and std 0.1
    y = x1**2 + x2**3 + noise

    # Optionally, combine x1 and x2 into a single feature array
    X = np.column_stack((x1, x2))
    data = pd.DataFrame({
        'feature1': x1,
        'feature2': x2,
        'target': y
    })
    return data

def plot_training_history(history: list):
    plt.plot(history)
    plt.title('Training Loss Over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Mean Squared Error (MSE)')
    plt.grid()
    plt.show()

def plot_data(data: pd.DataFrame):
    plt.scatter(data['feature1'], data['feature2'], c=data['target'], cmap='viridis', marker='o')
    plt.colorbar(label='Target Value')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Synthetic Data Visualization')
    plt.grid()
    plt.show()

def main():
    # Example data
    data = generate_synthetic_data(num_samples=100, num_features=2, noise_level=0.1)
    plot_data(data)
    # Prepare input and output
    X = data[['feature1', 'feature2']].values
    y = data['target'].values
    epochs = 1000
    batch_size = 10
    learning_rate = 0.01
    # Initialize weights and bias
    weights = np.array([[0.5], [0.5]])
    bias = np.array([0.0])
    np.random.seed(42)
    # Perform batch gradient descent
    weights, bias, history = batch_gradient_descent(learning_rate=learning_rate, batch_size=batch_size, X=X, y=y, weights=weights, bias=bias, epochs=epochs)
    # Make predictions
    predictions = predict(input = X, weights = weights, bias  = bias)
    
    plot_training_history(history)

    # Calculate MSE
    error = mse(actual = y, predicted = predictions)

    print(f"Mean Squared Error: {error}")


if __name__ == "__main__":
    main()