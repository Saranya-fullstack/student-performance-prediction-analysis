import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("dataset/student_data.csv")

X = df[[
    "study_hours",
    "attendance",
    "previous_marks",
    "assignment_score",
    "sleep_hours"
]]

y = df["final_marks"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training features:", X_train.shape)
print("Testing features:", X_test.shape)

print("Training target:", y_train.shape)
print("Testing target:", y_test.shape)