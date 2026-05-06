import pandas as pd
import numpy as np

# -------------------------------
# STEP 1: LOAD DATA
# -------------------------------
print("Loading dataset...")
df = pd.read_csv("customers-100.csv")   # change file name if needed

print("\nInitial Data Info:")
print(df.info())
print("\nFirst 5 rows:")
print(df.head())

# -------------------------------
# STEP 2: REMOVE DUPLICATES
# -------------------------------
print("\nChecking duplicates...")
print("Duplicate rows:", df.duplicated().sum())

df = df.drop_duplicates()

# -------------------------------
# STEP 3: DROP IRRELEVANT COLUMNS
# -------------------------------
# (Modify based on dataset)
cols_to_drop = []
for col in df.columns:
    if "id" in col.lower() and col != "customer_id":
        cols_to_drop.append(col)

df = df.drop(columns=cols_to_drop, errors='ignore')

# Rename columns (example)
df.columns = df.columns.str.lower().str.replace(" ", "_")

# -------------------------------
# STEP 4: HANDLE MISSING VALUES
# -------------------------------
print("\nMissing values before cleaning:")
print(df.isna().sum())

# Fill numeric columns with median
for col in df.select_dtypes(include=np.number).columns:
    df[col].fillna(df[col].median(), inplace=True)

# Fill categorical columns with mode
for col in df.select_dtypes(include='object').columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# Drop rows where critical columns are missing
if "customer_id" in df.columns:
    df.dropna(subset=["customer_id"], inplace=True)

print("\nMissing values after cleaning:")
print(df.isna().sum())

# -------------------------------
# STEP 5: DATA TYPE CONVERSION
# -------------------------------
for col in df.columns:
    # Convert date columns
    if "date" in col:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Convert numeric strings to numbers
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace(",", "")
        df[col] = pd.to_numeric(df[col], errors='ignore')

# -------------------------------
# STEP 6: FORMAT STANDARDIZATION
# -------------------------------
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.lower().str.strip()

# Example mapping
df.replace({
    "male": "Male",
    "m": "Male",
    "female": "Female",
    "f": "Female"
}, inplace=True)

# -------------------------------
# FINAL VALIDATION
# -------------------------------
print("\nFinal Data Info:")
print(df.info())

print("\nFinal duplicate check:", df.duplicated().sum())

# -------------------------------
# SAVE CLEAN DATA
# -------------------------------
df.to_csv("cleaned_data.csv", index=False)

print("\n✅ Data cleaning complete! File saved as cleaned_data.csv")