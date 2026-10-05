import pandas as pd

df = pd.read_csv("datasets/raw/insurance.csv")

print("FIRST 5 ROWS:")
print(df.head())

print("\nCOLUMN NAMES:")
print(df.columns)

print("\nDATASET SIZE:")
print(df.shape)

print("\nMISSING VALUES:")
print(df.isnull().sum())
print("\nSTATISTICAL SUMMARY:")
print(df.describe())
print("\nSEX VALUES:")
print(df["sex"].value_counts())

print("\nSMOKER VALUES:")
print(df["smoker"].value_counts())

print("\nREGION VALUES:")
print(df["region"].value_counts())
print("\nDATASET SHAPE:")
print(df.shape)

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\nDUPLICATE ROWS:")
print(df.duplicated().sum())

print("\nDATA TYPES:")
print(df.dtypes)

print("\nBASIC STATISTICS:")
print(df.describe())