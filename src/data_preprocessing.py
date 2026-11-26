import pandas as pd

# Load dataset
df = pd.read_csv("dataset/student_data.csv")

# Display all data
print(df)

# Display first 5 rows
print(df.head())

# Dataset shape
print(df.shape)

# Information about dataset
print(df.info())

# Statistical summary
print(df.describe())