import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# 1. Load dataset
data = pd.read_csv("datasets/health_insurance_13_features_dataset.csv")


# 2. Input features
X = data[
    [
        "Age",
        "Sex",
        "BMI",
        "Children",
        "Smoker",
        "Region",
        "Pre-existing Disease",
        "Previous Hospitalization",
        "Diagnosis",
        "Length of Stay",
        "Medical Expenses",
        "Coverage Amount",
        "Previous Claims"
    ]
]


# 3. Target
y = data["Insurance Charges"]


# 4. Categorical and numerical columns
categorical_columns = [
    "Sex",
    "Smoker",
    "Region",
    "Pre-existing Disease",
    "Previous Hospitalization",
    "Diagnosis"
]

numerical_columns = [
    "Age",
    "BMI",
    "Children",
    "Length of Stay",
    "Medical Expenses",
    "Coverage Amount",
    "Previous Claims"
]


# 5. Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_columns),
        ("numerical", "passthrough", numerical_columns)
    ]
)


# 6. Random Forest model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)


# 7. Complete pipeline
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# 8. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# 9. Train model
pipeline.fit(X_train, y_train)


# 10. Test model
predictions = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)


print("Model training completed!")
print("MAE:", round(mae, 2))
print("R2 Score:", round(r2 * 100, 2), "%")


# 11. Save model
joblib.dump(
    pipeline,
    "models/insurance_model_13_features.pkl"
)

print("Model saved successfully!")
print("File: models/insurance_model_13_features.pkl")