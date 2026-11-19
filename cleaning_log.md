# Data Cleaning Log

**Dataset:** Sample - Superstore.csv

## Before and after

| Check | Before | After |
|---|---|---|
| Rows | 9994 | 9994 |
| Columns | 21 | 22 |
| Missing cells | 0 | 0 |
| Duplicate rows | 0 | 0 |

## Issues found and decisions

1. **Missing values:** 0 missing cells found in the original file.
2. **Duplicates:** 0 duplicate rows found. Duplicates were removed.
3. **Text columns:** extra spaces removed from all text columns, and Ship Mode, Segment, Region, Category and Sub-Category set to Title Case. 16 cells were changed.
4. **Dates:** Order Date and Ship Date were stored as text. Converted to real dates.
5. **Outliers (IQR method on Sales):** limits are -271.71 to 498.93. 1167 orders (11.7%) are above the upper limit. Decision: values were capped in a new column, Sales_capped. The original Sales column was kept, because very large orders can be real and valid.
6. **Imputation practice:** on a copy of the data, 50 Profit values and 20 Segment values were removed on purpose. Profit was filled with mean, median and forward fill, and the results were compared. Segment was filled with the mode (the most common value). The real dataset was not changed.

## Decision rule I will use
For skewed number columns (like Profit and Sales) I prefer the median, because the mean is pulled by very large values. For text columns I use the mode.
