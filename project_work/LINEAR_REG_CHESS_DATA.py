import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import kagglehub

# Download latest version
# path = kagglehub.dataset_download("datasnaek/chess")

# print("Path to dataset files:", path)

df = pd.read_csv(r"C:\Users\User\.cache\kagglehub\datasets\datasnaek\chess\versions\1\games.csv")

# Determine the split index
split_index = len(df) // 6

# Split the DataFrame into two smaller DataFrames
df1 = df.iloc[:split_index]
df2 = df.iloc[split_index:]


# print("Shape of df1:", df1.shape)
# print("Shape of df2:", df2.shape)

# Create a figure with multiple subplots
fig, axs = plt.subplots(3, 2, figsize=(10, 8))

# Plot for df1
axs[0][0].scatter(df1.index, df1['white_rating'])
axs[0][0].set_title('Scatter plot for ratings')
axs[0][0].set_xlabel('Index')
axs[0][0].set_ylabel('White Rating')

# Plot for df2
axs[1][0].scatter(df1.index, df1['opening_eco'])
axs[1][0].set_title('Scatter plot for opening')
axs[1][0].set_xlabel('index')
axs[1][0].set_ylabel('Opening')

axs[2][0].scatter(df1.index, df1['opening_eco'])
axs[2][0].set_title('Scatter plot for opening')
axs[2][0].set_xlabel('index')
axs[2][0].set_ylabel('Opening')

axs[0][1].scatter(df1.index, df1['turns'])
axs[0][1].set_title('Scatter plot for opening')
axs[0][1].set_xlabel('index')
axs[0][1].set_ylabel('turns')

axs[1][1].scatter(df1['opening_eco'], df1['turns'])
axs[1][1].set_title('Scatter plot for opening')
axs[1][1].set_xlabel('opening')
axs[1][1].set_ylabel('turns')

# Adjust layout to prevent overlap
plt.tight_layout()

plt.show()