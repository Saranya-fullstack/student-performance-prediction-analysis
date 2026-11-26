import joblib
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_DIR / "models" / "random_forest_regression.joblib"

model = joblib.load(MODEL_PATH)

student = pd.DataFrame(
    [[6, 85, 75, 80, 7]],
    columns=[
        "study_hours",
        "attendance",
        "previous_marks",
        "assignment_score",
        "sleep_hours",
    ],
)

prediction = model.predict(student)

print("Predicted Final Marks:", prediction[0])