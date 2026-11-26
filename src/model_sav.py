import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier


# 1. Folder paths
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

DATA_PATH = PROJECT_DIR / "dataset" / "student_data.csv"
MODEL_DIR = PROJECT_DIR / "models"

MODEL_DIR.mkdir(exist_ok=True)


# 2. Load dataset
df = pd.read_csv("dataset/student_data.csv")

# 3. Select features
X = df[[
    "study_hours",
    "attendance",
    "previous_marks",
    "assignment_score",
    "sleep_hours"
]]

# 4. Regression target
y_regression = df["final_marks"]

# 5. Classification target
y_classification = (df["final_marks"] >= 50).astype(int)


# 6. Train-test split
X_train, X_test, y_train_reg, y_test_reg = train_test_split(
    X,
    y_regression,
    test_size=0.2,
    random_state=42
)


# Classification split
X_train_cls, X_test_cls, y_train_cls, y_test_cls = train_test_split(
    X,
    y_classification,
    test_size=0.2,
    random_state=42,
    stratify=y_classification
)


# =================================
# REGRESSION MODELS
# =================================

# Linear Regression
linear_model = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LinearRegression())
])

linear_model.fit(X_train, y_train_reg)


# Decision Tree Regression
tree_regression_model = DecisionTreeRegressor(
    max_depth=3,
    random_state=42
)

tree_regression_model.fit(X_train, y_train_reg)


# Random Forest Regression
forest_regression_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

forest_regression_model.fit(X_train, y_train_reg)


# =================================
# CLASSIFICATION MODELS
# =================================

# Logistic Regression
logistic_model = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression())
])

logistic_model.fit(X_train_cls, y_train_cls)


# Decision Tree Classification
tree_classification_model = DecisionTreeClassifier(
    max_depth=3,
    random_state=42
)

tree_classification_model.fit(X_train_cls, y_train_cls)


# Random Forest Classification
forest_classification_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

forest_classification_model.fit(X_train_cls, y_train_cls)


# =================================
# SAVE MODELS
# =================================

joblib.dump(
    linear_model,
    MODEL_DIR / "linear_regression.joblib"
)

joblib.dump(
    tree_regression_model,
    MODEL_DIR / "decision_tree_regression.joblib"
)

joblib.dump(
    forest_regression_model,
    MODEL_DIR / "random_forest_regression.joblib"
)

joblib.dump(
    logistic_model,
    MODEL_DIR / "logistic_regression.joblib"
)

joblib.dump(
    tree_classification_model,
    MODEL_DIR / "decision_tree_classifier.joblib"
)

joblib.dump(
    forest_classification_model,
    MODEL_DIR / "random_forest_classifier.joblib"
)

print("All models saved successfully!")


# =================================
# LOAD MODEL
# =================================

loaded_model = joblib.load(
    MODEL_DIR / "random_forest_regression.joblib"
)


# =================================
# PREDICTION
# =================================

new_student = pd.DataFrame(
    [[6, 85, 75, 80, 8]],
    columns=[
        "study_hours",
        "attendance",
        "previous_marks",
        "assignment_score",
        "sleep_hours"
    ]
)

prediction = loaded_model.predict(new_student)

print("Predicted Final Marks:", prediction[0])