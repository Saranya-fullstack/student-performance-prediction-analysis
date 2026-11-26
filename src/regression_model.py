import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

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
    X, y, test_size=0.2, random_state=42
)

# 1. Linear Regression
linear_model = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LinearRegression())
])

linear_model.fit(X_train, y_train)

# 2. Decision Tree
tree_model = DecisionTreeRegressor(
    max_depth=3,
    random_state=42
)

tree_model.fit(X_train, y_train)

# 3. Random Forest
forest_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

forest_model.fit(X_train, y_train)

# Prediction
linear_prediction = linear_model.predict(X_test)
tree_prediction = tree_model.predict(X_test)
forest_prediction = forest_model.predict(X_test)

print("Linear:", linear_prediction)
print("Decision Tree:", tree_prediction)
print("Random Forest:", forest_prediction)