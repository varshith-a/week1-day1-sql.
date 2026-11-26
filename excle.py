import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("indian_business_dataset.csv")

# Check the dataset
print(df.head())
print(df.info())

# Check missing values
print(df.isnull().sum())

# Remove duplicate rows
df = df.drop_duplicates()

# Revenue analysis
print(df.groupby("Region")["Revenue"].sum())

# Product analysis
print(df.groupby("Product")["Revenue"].sum())