import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("dataset/student_data.csv")

X = df[[
    "study_hours",
    "attendance",
    "previous_marks",
    "assignment_score",
    "sleep_hours"
]]

# Create classification target
y = (df["final_marks"] >= 50).astype(int)

# 1 = Pass
# 0 = Fail

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 1. Logistic Regression
logistic_model = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression())
])

logistic_model.fit(X_train, y_train)

# 2. Decision Tree Classifier
tree_model = DecisionTreeClassifier(
    max_depth=3,
    random_state=42
)

tree_model.fit(X_train, y_train)

# 3. Random Forest Classifier
forest_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

forest_model.fit(X_train, y_train)

# Predictions
logistic_prediction = logistic_model.predict(X_test)
tree_prediction = tree_model.predict(X_test)
forest_prediction = forest_model.predict(X_test)

print("Logistic Regression:", logistic_prediction)
print("Decision Tree:", tree_prediction)
print("Random Forest:", forest_prediction)