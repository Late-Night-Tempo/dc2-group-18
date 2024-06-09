# Imports
import pandas as pd
# Including as an import to remember to place it in requirements.txt
import openpyxl

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
# Use pyreadstat to open spss
import pyreadstat

# Use for question grouping
import re

# Sankey diagram or pcp
import plotly.graph_objects as go
import plotly.express as px

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder

# Collects the smaller year from the below llw database
def year_min(input_string):

    # Adjusted pattern to capture the year
    pattern = r'(\d{4})'

    # Use re.search to find the pattern anywhere in the string
    year_max = re.search(pattern, input_string)

    if year_max:
        year_max = year_max.group(1)
        year_min = int(year_max) - 1

        return year_min
    else:
        return None

# Collects the year as is from a string/column
def year_norm(input_string):

    # Adjusted pattern to capture the year
    pattern = r'(\d{4})'

    # Use re.search to find the pattern anywhere in the string
    year_max = re.search(pattern, input_string)

    if year_max:
        year_max = year_max.group(1)
        year_max = int(year_max)

        return year_max
    else:
        return None



# Collect dfs
pas_ward = pd.read_csv("CleanedDroppedPasWardData.csv")
question_dictionary = pd.read_excel("TrueFalseSetter.xlsx")
below_llw = pd.read_csv("CleanedBelowLLWBorough.csv")
trust_df = pd.read_csv("data/pas_data_borough.csv")

# Gender inac
econ_inac_fem = pd.read_csv("economically inactive females percentage.csv")
econ_inac_mal = pd.read_csv("economically inactive males percentage.csv")

# Weekly Income both
week_income = pd.read_excel("earnings-residence-borough.xlsx", sheet_name="Total, weekly")

# below llw + % inac + gender_inac + week income = prop
# second eq includes da questions

response_numerical = {
    np.nan: 0,
    "Not Asked": 0,
    "Very important": 2,
    'Fairly important': 1,
    'Not very important': -1,
    'Not at all important': -2,

    'Agree': 2,
    'Neither agree nor disagree': 0,
    'Strongly agree': 1,
    'Disagree': -1,
    'Strongly disagree': -2,

    'Tend to agree': 1,
    'Tend to disagree': -1,

    "Don't know": 0,
    'Refused': 0,

    'Not a problem at all': 2,
    'Not a very big problem': 1,
    'Fairly big problem': -1,
    'Very big problem': -2,

    'Not very worried': 1,
    'Fairly worried': -1,
    'Not at all worried': 2,
    'Very worried': -2,

    'More safe': 1,
    'It makes no difference': 0,
    'Less safe': -1,

    'Very safe': 2,
    'Fairly safe': 1,
    'A bit unsafe': -1,
    'Not at all safe': -2,
    'Completely satisfied': 3,
    'Very satisfied': 2,

    'Neither satisfied nor dissatisfied': 0,
    'Fairly satisfied': 1,
    'Completely dissatisfied': -3,
    'Fairly dissatisfied': -1,
    'Very dissatisfied': -2,

    'Good': 1,
    'Excellent': 2,
    'Fair': 0,
    'Very poor': -1,
    'Poor': -2,

}

#question_list = ["NQ135BD", "NQ21", "Q61", "Q62A", "Q62TI"]
question_list = ["C2;3", "NQ135BD;377", "NQ21;55", "Q61;97", "Q62A;98", "Q62TI;106", "MONTH_YEAR", "MONTH", "YEAR"]

 # Collect month + year
pas_ward["MONTH_YEAR"] = pas_ward["MONTH"].str.extract(r'\(([^)]+)\)')
pas_ward["YEAR"] = pd.to_datetime(pas_ward["MONTH_YEAR"]).dt.year

# Set pas_ward to only questions in question list
pas_ward = pas_ward[question_list]
pas_ward.rename(columns={"C2;3": "Area Name"}, inplace=True)


## Begin attatching other datasets to current dataset

# basically: check all unique years for responses in a certain question(?)
# From that, collect the corresponding data points to each borough
# and then get frequency of unique per question
# turn it into model, like:
# A*freqA + B*freqB + C*freqC = Y (resulting data)
# Or perhaps use questions themselves as coefficients

# LLW column time:

# Rename below LLW cols
for columns in below_llw.columns:
    year_name = year_min(columns)
    if year_name:
        below_llw.rename(columns={columns: year_name}, inplace=True)
below_llw.drop(columns=["Unnamed: 0", "Code"], inplace=True)

# Rename econ inac fem cols
for columns in econ_inac_fem.columns:
    year_name = year_norm(columns)
    if year_name:
        econ_inac_fem.rename(columns={columns: year_name}, inplace=True)

econ_inac_fem.drop(columns=["Unnamed: 0"], inplace=True)

# Rename econ inac mal cols
for columns in econ_inac_mal.columns:
    year_name = year_norm(columns)
    if year_name:
        econ_inac_mal.rename(columns={columns: year_name}, inplace=True)
econ_inac_mal.drop(columns=["Unnamed: 0"], inplace=True)

# Rename week income cols
for columns in week_income.columns:
    columns = str(columns)
    if "Unnamed" in columns or "Code" in columns:
        week_income.drop(columns=[columns], inplace=True)


# remove "pay" listings and city of london
week_income = week_income.truncate(before=3, after=34)
econ_inac_fem = econ_inac_fem.truncate(before=1)
econ_inac_mal = econ_inac_mal.truncate(before=1)




# Add proportion. proportion shall be our lovely y variable. the questions will indicate the predicting vars
# Although we will need to separate the measures... make multiple models, one per each measure!
trust_merge = trust_df.drop(columns=["Unnamed: 0", "Survey", "MPS"])
trust_merge.rename(columns={"Borough": "Area Name", "Date":"YEAR"}, inplace=True)
trust_merge["YEAR"] = pd.to_datetime(trust_merge["YEAR"])
trust_merge["YEAR"] = trust_merge["YEAR"].dt.year


# Now all the column names are just the year, yippee
# Now we match borough and year together, and create LLW and Percent inactivity column

 # Collect month + year
pas_ward["MONTH_YEAR"] = pas_ward["MONTH"].str.extract(r'\(([^)]+)\)')
pas_ward["YEAR"] = pd.to_datetime(pas_ward["MONTH_YEAR"]).dt.year

# Reshape DataFrame LLW from wide to long format
df_B_long = below_llw.melt(id_vars=['Area Name'], var_name='YEAR', value_name='LLW')
df_B_long['YEAR'] = df_B_long['YEAR'].astype(int)


# Reshape DataFrame Inactivity fem from wide to long format
df_inac_long_fem = econ_inac_fem.melt(id_vars=['Area'], var_name='YEAR', value_name='Inac_Perc_Fem')
df_inac_long_fem.rename(columns={"Area": "Area Name"}, inplace=True)
df_inac_long_fem['YEAR'] = df_inac_long_fem['YEAR'].astype(int)


# Reshape DataFrame Inactivity mal from wide to long format
df_inac_long_mal = econ_inac_mal.melt(id_vars=['Area'], var_name='YEAR', value_name='Inac_Perc_Mal')
df_inac_long_mal.rename(columns={"Area": "Area Name"}, inplace=True)
df_inac_long_mal['YEAR'] = df_inac_long_mal['YEAR'].astype(int)


# Reshape DataFrame Weekly Income from wide to long format
df_week_inc_long = week_income.melt(id_vars=['Area'], var_name='YEAR', value_name='Week_Inc')
df_week_inc_long.rename(columns={"Area": "Area Name"}, inplace=True)
df_week_inc_long['YEAR'] = df_week_inc_long['YEAR'].astype(int)


# Merge DataFrame Pas and LLW
pas_merged_incom = pd.merge(pas_ward, df_B_long, on=['Area Name', 'YEAR'])


# Merge pas and inac
pas_logistic = pd.merge(pas_merged_incom, df_inac_long_fem, on=["Area Name", "YEAR"])
pas_logistic = pd.merge(pas_logistic, df_inac_long_mal, on=["Area Name", "YEAR"])
pas_logistic = pd.merge(pas_logistic, df_week_inc_long, on=["Area Name", "YEAR"])


# Merge pas and trust

# We will merge using proportion, not MPS
# Drop duplicates
trust_merge.drop_duplicates(inplace=True)

# Use pivot_table to pivot the DataFrame
df_pivot = trust_merge.pivot_table(index=['YEAR', 'Area Name'], columns='Measure', values='Proportion', aggfunc='first').reset_index()

# Flatten the columns
df_pivot.columns.name = None
df_pivot.columns = df_pivot.columns.map(str)

# Reset the index to flatten the DataFrame
df_pivot.reset_index(inplace=True, drop=True)

# Merge new pivot with proportion data into pas_logistic
pas_logistic = pd.merge(pas_logistic, df_pivot, on=["Area Name", "YEAR"])

#print(pas_logistic)
pas_logistic.to_csv("LregPasData.csv", index=False)

# Set targets and inputs
target_category = "Trust MPS"
limited_global_cols = ["YEAR","LLW","Inac_Perc_Fem","Inac_Perc_Mal","Week_Inc", target_category]
input_cols = ["YEAR","LLW","Inac_Perc_Fem","Inac_Perc_Mal","Week_Inc"]
all_global_cols = ["YEAR","LLW","Inac_Perc_Fem","Inac_Perc_Mal","Week_Inc", "NQ135BD;377", "NQ21;55", "Q61;97", "Q62A;98", "Q62TI;106", target_category]
input_and_q_cols = ["YEAR","LLW","Inac_Perc_Fem","Inac_Perc_Mal","Week_Inc", "NQ135BD;377", "NQ21;55", "Q61;97", "Q62A;98", "Q62TI;106"]

# Filter to include only the current categories and target category. Drop nans.
pas_logistic_filtered = pas_logistic[limited_global_cols].copy().dropna(subset=[target_category])

# Set x and y
X = pas_logistic_filtered[input_cols]
y = pas_logistic_filtered[target_category]

# Train-test split
# use random_state to act as a seed, if needed
# test_size defaults to .25, so 25% of data is used as test data
X_train, X_test, y_train, y_test = train_test_split(X, y)

# Create and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Extract coefficients and corresponding feature names
coefficients = pd.Series(model.coef_, index=X.columns)

# Identify the category with the largest absolute value coefficient
largest_abs_coefficient = coefficients.abs().idxmax()
largest_abs_value = coefficients[largest_abs_coefficient]

# Print details of the linear regression model
print("GLOBAL BASIC REGRESSION")
print(f"Category: {input_cols}")
print(f"Target Category: {target_category}")
print(f"The category with the largest absolute value coefficient is: {largest_abs_coefficient}")
print(f"The coefficient value is: {largest_abs_value}")
print("Intercept:", model.intercept_)
print("Coefficients:", model.coef_)
print("R-squared:", model.score(X, y))
print()

# Drop rows with NaN in the target category
pas_logistic_question_filtered = pas_logistic[all_global_cols].copy().dropna(subset=[target_category])

# Encode categorical variables using OrdinalEncoder
ordinal_encoder = OrdinalEncoder()
categorical_columns = ["NQ135BD;377", "NQ21;55", "Q61;97", "Q62A;98", "Q62TI;106"]
pas_logistic_question_filtered[categorical_columns] = ordinal_encoder.fit_transform(pas_logistic_question_filtered[categorical_columns].astype(str))

# Set X and y
input_and_q_cols = [col for col in all_global_cols if col != target_category]
X2 = pas_logistic_question_filtered[input_and_q_cols]
y2 = pas_logistic_question_filtered[target_category]

# Train-test split
# use random_state to act as a seed, if needed
# test_size defaults to .25, so 25% of data is used as test data
X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2)

# Create and train the linear regression model
model2 = LinearRegression()
model2.fit(X2_train, y2_train)

# Extract coefficients and corresponding feature names
coefficients2 = pd.Series(model2.coef_, index=X2.columns)

# Identify the category with the largest absolute value coefficient
largest_abs_coefficient2 = coefficients2.abs().idxmax()
largest_abs_value2 = coefficients2[largest_abs_coefficient2]

# Print details of the linear regression model
print("GLOBAL QUESTIONS ADDED REGRESSION")
print(f"Category: {input_and_q_cols}")
print(f"Target Category: {target_category}")
print(f"The category with the largest absolute value coefficient is: {largest_abs_coefficient2}")
print(f"The coefficient value is: {largest_abs_value2}")
print("Intercept:", model2.intercept_)
print("Coefficients:", model2.coef_)
print("R-squared:", model2.score(X2, y2))
print()