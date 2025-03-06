import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
from scipy.stats import pearsonr
import statsmodels.api as sm

file1 = "Immunization expenditure.xlsx"
file2 = "Infectious Disease.csv"

df_immunization = pd.read_excel(file1, sheet_name=0)  # Load immunization expenditure data
df_disease = pd.read_csv(file2)  # Load infectious disease data

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Convert the 'VALUE' column to numeric; non-numeric entries become NaN.
df_immunization['VALUE'] = pd.to_numeric(df_immunization['VALUE'], errors='coerce')

# Optionally filter for a specific indicator (e.g., vaccine spending)
df_immunization_vacc = df_immunization[df_immunization['INDCODE'] == 'FIN_GVT_VACC'].copy()

# Group by 'COUNTRYNAME' and 'YEAR' and sum up the expenditure values.
df_immunization_grouped = (
    df_immunization_vacc
    .dropna(subset=['VALUE'])  # Keep rows with valid numeric values.
    .groupby(['COUNTRYNAME', 'YEAR'], as_index=False)['VALUE']
    .sum()
)

# Rename the 'VALUE' column to 'EXPENDITURE' for clarity.
df_immunization_grouped.rename(columns={"VALUE": "IMMUNISATION_EXPENDITURE"}, inplace=True)

# Inspect the grouped expenditure data.
print("Grouped Expenditure Data:")
print(df_immunization_grouped.head())
print("df_immunization_grouped columns:", df_immunization_grouped.columns.tolist())

# Standardize column names: remove extra spaces and convert to uppercase.
df_disease.columns = df_disease.columns.str.strip().str.upper()
print("df_disease columns after standardization:", df_disease.columns.tolist())

# Rename columns to match the expenditure DataFrame.
df_disease.rename(columns={
    "PERIOD": "YEAR",
    "LOCATION": "COUNTRYNAME",
    "FACTVALUENUMERIC": "DISEASE_CASES"
}, inplace=True)
print("df_disease columns after renaming:", df_disease.columns.tolist())

# Merge the expenditure data with disease data on COUNTRYNAME and YEAR.
df_merged = pd.merge(df_immunization_grouped, df_disease, on=["YEAR", "COUNTRYNAME"], how="inner")

# Optionally drop rows with missing disease case data
df_merged = df_merged.dropna(subset=['DISEASE_CASES'])

# Inspect the merged dataset
print("Merged Data:")
print(df_merged.head())

top_countries = (
    df_merged.groupby("COUNTRYNAME")["IMMUNISATION_EXPENDITURE"].sum()
    .nlargest(4)  # Get top 4 highest total expenditure countries
    .index.tolist()
)

# Filter merged data for the top countries and sort by COUNTRYNAME and YEAR
df_selected = df_merged[df_merged['COUNTRYNAME'].isin(top_countries)].copy()

# Sort the data for consistent plotting
df_selected.sort_values(['COUNTRYNAME', 'YEAR'], inplace=True)

# Define ASEAN countries (adjust the list as needed)
asean_countries = ['Indonesia', 'Malaysia', 'Philippines', 'Singapore', 'Thailand', 'Vietnam', 'Brunei', 'Cambodia', 'Laos', 'Myanmar']

# Filter the merged dataset for ASEAN countries only
df_asean = df_merged[df_merged['COUNTRYNAME'].isin(asean_countries)].copy()

# Plotting Disease Cases Over Time for ASEAN Countries
plt.figure(figsize=(12, 8))
sns.lineplot(data=df_asean, x='YEAR', y='DISEASE_CASES', hue='COUNTRYNAME', marker='o')
plt.title('Disease Cases Over Time - ASEAN Countries')
plt.xlabel('Year')
plt.ylabel('Disease Cases')
plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
g2 = sns.FacetGrid(df_selected, col="COUNTRYNAME", col_wrap=2, height=4, sharey=False)
g2.map(sns.lineplot, "YEAR", "DISEASE_CASES", marker="s", color="red")
g2.fig.suptitle("Trends in Disease Cases Over Time (Top 4 Countries)", y=1.05)
g2.set_axis_labels("Year", "Disease Cases")
plt.tight_layout()
plt.show()

# Filter the merged dataset for ASEAN countries only
asean_countries = ['Indonesia', 'Malaysia', 'Philippines', 'Singapore', 'Thailand', 'Vietnam', 'Brunei', 'Cambodia', 'Laos', 'Myanmar']
df_asean = df_merged[df_merged['COUNTRYNAME'].isin(asean_countries)].copy()

# Create a FacetGrid to show each country's immunisation expenditure over time
plt.figure(figsize=(14, 10))
g = sns.FacetGrid(df_asean, col="COUNTRYNAME", col_wrap=3, sharey=False, height=4)
g.map(sns.lineplot, "YEAR", "IMMUNISATION_EXPENDITURE", marker="o")
g.set_titles("{col_name}")
g.set_axis_labels("Year", "Immunisation Expenditure")
g.fig.suptitle("Immunisation Expenditure Over Time - ASEAN Countries", y=1.02)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
g = sns.FacetGrid(df_selected, col="COUNTRYNAME", col_wrap=2, height=4, sharey=False)
g.map(sns.lineplot, "YEAR", "IMMUNISATION_EXPENDITURE", marker="o")
g.fig.suptitle("Trends in Immunisation Expenditure Over Time (Top 4  Countries)", y=1.05)
g.set_axis_labels("Year", "Immunisation Expenditure")
plt.tight_layout()
plt.show()

#Filter Data for Preventive and Total Healthcare Spending

# Assuming your original DataFrame is named df_immunization
df_preventive = df_immunization[df_immunization['INDCODE'] == 'FIN_GVT_VACC'].copy()
df_total = df_immunization[df_immunization['INDCODE'] == 'FIN_GVT_RI'].copy()

# Group Data by COUNTRYNAME and YEAR

# Group preventive spending data and rename the VALUE column
df_preventive_grouped = (
    df_preventive.dropna(subset=['VALUE'])
    .groupby(['COUNTRYNAME', 'YEAR'], as_index=False)['VALUE']
    .sum()
)
df_preventive_grouped.rename(columns={"VALUE": "PREVENTIVE_SPENDING"}, inplace=True)

# Group total healthcare spending data and rename the VALUE column
df_total_grouped = (
    df_total.dropna(subset=['VALUE'])
    .groupby(['COUNTRYNAME', 'YEAR'], as_index=False)['VALUE']
    .sum()
)
df_total_grouped.rename(columns={"VALUE": "TOTAL_HEALTHCARE_SPENDING"}, inplace=True)

# Merge the Two Datasets on COUNTRYNAME and YEAR
df_spending = pd.merge(df_preventive_grouped, df_total_grouped, on=['COUNTRYNAME', 'YEAR'], how='inner')

# Calculate Treatment Spending and Combined Total
df_spending['TREATMENT_SPENDING'] = df_spending['TOTAL_HEALTHCARE_SPENDING'] - df_spending['PREVENTIVE_SPENDING']

# Calculate the Combined Total (Preventive + Treatment Spending)
df_spending['COMBINED_TOTAL'] = df_spending['PREVENTIVE_SPENDING'] + df_spending['TREATMENT_SPENDING']


# Calculate the percentage of the combined total for each spending type
df_spending['PREVENTIVE_SPENDING_PERCENT'] = (df_spending['PREVENTIVE_SPENDING'] / df_spending['COMBINED_TOTAL']) * 100
df_spending['TREATMENT_SPENDING_PERCENT'] = (df_spending['TREATMENT_SPENDING'] / df_spending['COMBINED_TOTAL']) * 100

# Calculate the ratio between preventive and treatment spending.
# Replace division-by-zero (which would produce infinite values) with 0.
df_spending['PREVENTIVE_TREATMENT_RATIO'] = np.where(
    df_spending['TREATMENT_SPENDING'] == 0,
    0,
    df_spending['PREVENTIVE_SPENDING'] / df_spending['TREATMENT_SPENDING']
)

#Display the Results
print(df_spending[['COUNTRYNAME', 'YEAR', 'PREVENTIVE_SPENDING_PERCENT', 
                   'TREATMENT_SPENDING_PERCENT', 'PREVENTIVE_TREATMENT_RATIO']].head())

# Filter for ASEAN Countries Only
# Define the list of ASEAN countries (adjust names as needed to match your data)
asean_countries = [
    "Brunei", "Cambodia", "Indonesia", "Laos", 
    "Malaysia", "Myanmar", "Philippines", "Singapore", 
    "Thailand", "Vietnam"
]
df_asean = df_spending[df_spending['COUNTRYNAME'].isin(asean_countries)]

# Graph 2: Time Series Analysis for ASEAN Countries
plt.figure(figsize=(12, 8))
for country in df_asean['COUNTRYNAME'].unique():
    df_country = df_asean[df_asean['COUNTRYNAME'] == country]
    # Plot preventive spending over time
    plt.plot(df_country['YEAR'], df_country['PREVENTIVE_SPENDING_PERCENT'], 
             marker='o', label=f'{country} - Preventive')
    # Plot treatment spending over time
    plt.plot(df_country['YEAR'], df_country['TREATMENT_SPENDING_PERCENT'], 
             marker='x', label=f'{country} - Treatment')

plt.xlabel('Year')
plt.ylabel('Spending Percentage')
plt.title('Time Series of Preventive and Treatment Spending Percentages for ASEAN Countries')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Detailed Visualization for Myanmar

# Filter for Myanmar only from the ASEAN dataset
df_Myanmar = df_asean[df_asean['COUNTRYNAME'] == 'Myanmar']

plt.figure(figsize=(10, 6))
plt.plot(df_Myanmar['YEAR'], df_Myanmar['PREVENTIVE_SPENDING_PERCENT'], 
         marker='o', linestyle='-', label='Preventive Spending %', color='green')
plt.plot(df_Myanmar['YEAR'], df_Myanmar['TREATMENT_SPENDING_PERCENT'], 
         marker='x', linestyle='--', label='Treatment Spending %', color='blue')

plt.xlabel('Year', fontsize=12)
plt.ylabel('Spending Percentage', fontsize=12)
plt.title('Myanmar: Preventive vs Treatment Spending Over Years', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True)
plt.tight_layout()
plt.show()

# Filter for ASEAN Countries Only

# Define the list of ASEAN countries
asean_countries = [
    "Brunei", "Cambodia", "Indonesia", "Laos", 
    "Malaysia", "Myanmar", "Philippines", "Singapore", 
    "Thailand", "Vietnam"
]
df_asean = df_spending[df_spending['COUNTRYNAME'].isin(asean_countries)]

# Detailed Bar Graph for Myanmar
# Filter for Myanmar only and sort by YEAR
df_Myanmar = df_asean[df_asean['COUNTRYNAME'] == 'Myanmar'].sort_values('YEAR')

# Create a grouped bar graph comparing Preventive vs. Treatment Spending Percentages over the years
plt.figure(figsize=(10,6))
index = np.arange(len(df_Myanmar))
bar_width = 0.35

plt.bar(index, df_Myanmar['PREVENTIVE_SPENDING_PERCENT'], bar_width, 
        label='Preventive Spending %', color='green')
plt.bar(index + bar_width, df_Myanmar['TREATMENT_SPENDING_PERCENT'], bar_width, 
        label='Treatment Spending %', color='blue')

plt.xlabel('Year', fontsize=12)
plt.ylabel('Spending Percentage', fontsize=12)
plt.title('Myanmar: Preventive vs Treatment Spending Over Years', fontsize=14)
plt.xticks(index + bar_width / 2, df_Myanmar['YEAR'])
plt.legend()
plt.tight_layout()
plt.show()

# Load the datasets
df_expenditure = pd.read_excel("Immunization expenditure.xlsx", sheet_name="Sheet1")
df_disease = pd.read_csv("Infectious Disease.csv")

# Filter for vaccine spending
df_vaccine_spending = df_expenditure[df_expenditure['INDCODE'] == 'FIN_GVT_VACC'].copy()

# Keep only relevant columns and rename them to match the disease dataset
df_vaccine_spending = df_vaccine_spending[['COUNTRYNAME', 'YEAR', 'VALUE']]
df_vaccine_spending.rename(columns={'COUNTRYNAME': 'Location', 'YEAR': 'Period', 'VALUE': 'Vaccine_Spending'}, inplace=True)

# Ensure the year is an integer for merging
df_vaccine_spending['Period'] = df_vaccine_spending['Period'].astype(int)

# Load the datasets (make sure these files are in your working directory)
df_expenditure = pd.read_excel("Immunization expenditure.xlsx", sheet_name="Sheet1")
df_disease = pd.read_csv("Infectious Disease.csv")

# We filter the expenditure dataset for government vaccine spending (INDCODE = 'FIN_GVT_VACC')
# rename columns for consistency.

# Filter for vaccine spending
df_vaccine_spending = df_expenditure[df_expenditure['INDCODE'] == 'FIN_GVT_VACC'].copy()

# Keep only relevant columns and rename them to match the disease dataset
df_vaccine_spending = df_vaccine_spending[['COUNTRYNAME', 'YEAR', 'VALUE']]
df_vaccine_spending.rename(columns={'COUNTRYNAME': 'Location', 'YEAR': 'Period', 'VALUE': 'Vaccine_Spending'}, inplace=True)

# Ensure the year is an integer for merging
df_vaccine_spending['Period'] = df_vaccine_spending['Period'].astype(int)

# We select and rename columns so they match the vaccine spending data.

df_vaccine_coverage = df_disease[['Location', 'Period', 'Value']].copy()
df_vaccine_coverage.rename(columns={'Value': 'Vaccination_Coverage'}, inplace=True)
df_vaccine_coverage['Period'] = df_vaccine_coverage['Period'].astype(int)

# Merge the two datasets on `Location` (country) and `Period` (year).

# %%
df_merged = pd.merge(df_vaccine_spending, df_vaccine_coverage, on=['Location', 'Period'], how='inner')

# Convert spending and coverage to numeric values (handle any errors)
df_merged['Vaccine_Spending'] = pd.to_numeric(df_merged['Vaccine_Spending'], errors='coerce')
df_merged['Vaccination_Coverage'] = pd.to_numeric(df_merged['Vaccination_Coverage'], errors='coerce')

# Drop rows with missing values in key columns
df_merged.dropna(subset=['Vaccine_Spending', 'Vaccination_Coverage'], inplace=True)

# View a preview of the merged dataset
df_merged.head()

# Indicator Analysis: Correlation and Regression
# Here we compute:
# - Pearson’s correlation coefficient and its p-value.
# - A linear regression model (using Ordinary Least Squares) to quantify the relationship.

# %%
# Pearson Correlation
corr, p_val = pearsonr(df_merged['Vaccine_Spending'], df_merged['Vaccination_Coverage'])
print("Pearson correlation coefficient:", corr)
print("p-value:", p_val)

# Linear Regression Analysis
X = sm.add_constant(df_merged['Vaccine_Spending'])  # Add constant term for intercept
y = df_merged['Vaccination_Coverage']
model = sm.OLS(y, X).fit()  # Fit the model
print(model.summary())

# Visualization: Scatter Plot with Regression Line
# A scatter plot with the regression line to help with the visualization of the relationship. 
# We use a logarithmic scale on spending due to its wide range.

plt.figure(figsize=(10,6))
sns.regplot(x='Vaccine_Spending', y='Vaccination_Coverage', data=df_merged, scatter_kws={'alpha': 0.5}, line_kws={"color": "red"})
plt.xlabel("Government Vaccine Spending ($)")
plt.ylabel("Vaccination Coverage (%)")
plt.title("Relationship Between Vaccine Spending and Vaccination Coverage")
plt.xscale('log')  # Apply log scale for clarity
plt.grid(True)
plt.show()
