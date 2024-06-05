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


def group_consecutive_matches(strings):
    groups = []
    current_group = []

    for string in strings:
        if not current_group:
            current_group.append(string)
        else:
            # Check if the current string starts with the same prefix as the last string in the current group
            # Assuming the prefix is the first part until the first digit is encountered
            prefix_last = re.match(r'^\D*\d*', current_group[-1]).group()
            prefix_current = re.match(r'^\D*\d*', string).group()

            if prefix_current == prefix_last:
                current_group.append(string)
            else:
                groups.append(current_group)
                current_group = [string]

    if current_group:
        groups.append(current_group)

    return groups


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



# Collect dfs
pas_ward = pd.read_csv("CleanedDroppedPasWardData.csv")
question_dictionary = pd.read_excel("TrueFalseSetter.xlsx")
below_llw = pd.read_csv("CleanedBelowLLWBorough.csv")
inactivity_df = pd.read_csv("CleanedInactivityData.csv")

#print(below_llw)
# print(inactivity_df.columns)

# Group questions together and drop any unecessary columns
question_groups = []

for column in pas_ward.columns:
    unique_values = pas_ward[column].unique()
    unique_count = pas_ward[column].nunique()
    value_frequencies = pas_ward[column].value_counts()

    # Get all questions from dictionary
    if ";" in column:
        index = int(column.split(";")[1])
        question = str(column.split(";")[0])
        # print("Question:", question_dictionary["Question Content"][index])
        question_groups.append(column)

    # If accidental unnamed columns, remove
    if "Unnamed" in column:
        pas_ward.drop(columns=column, inplace=True)

# Process list to create grouped questions
grouped_matches = group_consecutive_matches(question_groups)
#print(grouped_matches)

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

question_reduced_list = ["NQ2B;6", "NQ2H;12", "NQ2I;13", "Q60;96"]


## Begin attatching other datasets to current dataset

# basically: check all unique years for responses in a certain question(?)
# From that, collect the corresponding data points to each borough
# and then get frequency of unique per question
# turn it into model, like:
# A*freqA + B*freqB + C*freqC = Y (resulting data)
# Or perhaps use questions themselves as coefficients

# LLW column time:
below_llw_shaper = below_llw.copy()
for columns in below_llw_shaper.columns:

    year_name = year_min(columns)

    if year_name:
        below_llw_shaper.rename(columns={columns: year_name}, inplace=True)

below_llw_shaper.drop(columns=["Unnamed: 0", "Code"], inplace=True)


# Inactivity column time
inactivity_df_shaper = inactivity_df.copy()
for columns in inactivity_df_shaper.columns:
    year_check = year_min(columns)


    if year_check:
        current_year = year_check + 1

        if "percent" not in columns:
            inactivity_df_shaper.drop(columns=[columns], inplace=True)
        else:
            inactivity_df_shaper.rename(columns={columns: current_year}, inplace=True)

inactivity_df_shaper.drop(columns=["Unnamed: 0", "Code"], inplace=True)



# Now all the column names are just the year, yippee
# Now we match borough and year together, and create LLW and Percent inactivity column


 # Collect month + year
pas_ward["MONTH_YEAR"] = pas_ward["MONTH"].str.extract(r'\(([^)]+)\)')
pas_ward["YEAR"] = pd.to_datetime(pas_ward["MONTH_YEAR"]).dt.year

# Reshape DataFrame LLW from wide to long format
df_B_long = below_llw_shaper.melt(id_vars=['Area Name'], var_name='YEAR', value_name='LLW')
df_B_long['YEAR'] = df_B_long['YEAR'].astype(int)


# Reshape DataFrame Inactivity from wide to long format
df_inac_long = inactivity_df_shaper.melt(id_vars=['Area'], var_name='YEAR', value_name='Inac_Perc')
df_inac_long.rename(columns={"Area": "Area Name"}, inplace=True)
df_inac_long['YEAR'] = df_inac_long['YEAR'].astype(int)


pas_ward.rename(columns={"C2;3": "Area Name"}, inplace=True)

# Merge DataFrame Pas and LLW
pas_merged_incom = pd.merge(pas_ward, df_B_long, on=['Area Name', 'YEAR'])


# Merge pas and inac
pas_logistic = pd.merge(pas_merged_incom, df_inac_long, on=["Area Name", "YEAR"])

print("Finished pas merged:")

print(pas_logistic)
pas_logistic.to_csv("LregPasData.csv", index=False)

# Sample DataFrame
data = {
    'Category': ['A', 'B', 'A', 'C', 'B', 'C', 'A', 'B', 'C', 'A'],
    'Value': [10, 15, 14, 10, 21, 20, 13, 19, 22, 15],
    'Target': [100, 150, 110, 130, 170, 180, 115, 165, 190, 120]
}
df = pd.DataFrame(data)

# Step 2: Identify unique values in the 'Category' column
unique_values = df['Category'].unique()

# Step 3: Create dummy variables (one-hot encoding)
df_dummies = pd.get_dummies(df, columns=['Category'], drop_first=True)

# Step 4: Prepare the data for regression
X = df_dummies.drop(columns='Target')  # Feature matrix (independent variables)
y = df_dummies['Target']               # Target variable (dependent variable)

# Step 5: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Create and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 7: Extract coefficients and corresponding feature names
coefficients = pd.Series(model.coef_, index=X.columns)

# Step 8: Identify the category with the largest absolute value coefficient
largest_abs_coefficient = coefficients.abs().idxmax()
largest_abs_value = coefficients[largest_abs_coefficient]

print(f"The category with the largest absolute value coefficient is: {largest_abs_coefficient}")
print(f"The coefficient value is: {largest_abs_value}")