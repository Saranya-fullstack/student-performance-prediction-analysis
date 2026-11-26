import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("dataset/student_data.csv")

# Select features
X = df[[
    "study_hours",
    "attendance",
    "previous_marks",
    "assignment_score",
    "sleep_hours"
]]

# Select target
y = df["final_marks"]

# Standardization
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("Original Features:")
print(X)

print("\nScaled Features:")
print(X_scaled)

print("\nTarget:")
print(y)