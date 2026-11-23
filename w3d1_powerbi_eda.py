
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

# Load the dataset
df = pd.read_csv("indian_sales_practice.csv")

# 1. Display first 5 rows
print("First 5 rows:")
print(df.head())

# 2. Dataset shape
print("\nDataset shape:")
print(df.shape)

# 3. Column information
print("\nDataset information:")
df.info()

# 4. Missing values
print("\nMissing values:")
print(df.isnull().sum())

# 5. Duplicate rows
print("\nDuplicate rows:")
print(df.duplicated().sum())

# 6. Summary statistics
print("\nSummary statistics:")
print(df.describe(include="all"))

# 7. Analyze categorical columns
categorical_columns = df.select_dtypes(
    include="object"
).columns

for column in categorical_columns[:3]:
    print(f"\nTop values in {column}:")
    print(df[column].value_counts().head(10))

# 8. Plot a numeric column
numeric_columns = df.select_dtypes(
    include=np.number
).columns

if len(numeric_columns) > 0:
    column = numeric_columns[0]

    df[column].dropna().plot(
        kind="hist",
        bins=20,
        title=f"Distribution of {column}"
    )

    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()
