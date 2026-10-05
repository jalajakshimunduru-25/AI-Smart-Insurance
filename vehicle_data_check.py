import pandas as pd

# Load vehicle insurance dataset
df = pd.read_csv("datasets/car_insurance_premium_dataset.csv")

print("DATASET SHAPE:")
print(df.shape)

print("\nCOLUMN NAMES:")
print(df.columns)

print("\nFIRST 5 ROWS:")
print(df.head())

print("\nMISSING VALUES:")
print(df.isnull().sum())