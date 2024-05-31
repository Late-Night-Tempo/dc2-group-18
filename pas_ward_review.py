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


def find_year(*args):
    all_years = []

    # Define the regex pattern for matching years
    pattern = r'\b(\d{4})\b'

    for text in args:
        # Find all 4-digit years in the text
        years = re.findall(pattern, text)

    return years[0]

# Collect dfs
pas_ward = pd.read_csv("CleanedDroppedPasWardData.csv")
question_dictionary = pd.read_excel("TrueFalseSetter.xlsx")
below_llw = pd.read_csv("CleanedBelowLLWBorough.csv")
inactivity_df = pd.read_csv("CleanedInactivityData.csv")

print(below_llw)
print(inactivity_df)

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
print(grouped_matches)

#########
# Begin analyzing pas dataset
#########


# Use test question before doing it automatically
test_question = "NQ2B;6"
borough = "Westminster - North"

# Okay SO because I AM DYING allow me to make a dictionary
# If thing is bad, subtract points. If thing is good, add points. Change nothing if not asked.
# If positive/negative needs to be changed, just multiply it by -1

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


for cols in question_reduced_list:
    print(cols)

# Goal:
# Find matching borough between all 3 datasets
# Find matching year
# get correlation between majority of responses and the inactivity and below llw



# print(pas_ward["BOROUGHNEIGHBOURHOOD;1"].unique())

# # Making graphs is a bad idea.
# for questions in question_reduced_list:
#     for borough in pas_ward["BOROUGHNEIGHBOURHOOD;1"].unique():
#
#         # Collect month + year
#         pas_ward["MONTH_YEAR"] = pas_ward["MONTH_YEAR"] = pas_ward["MONTH"].str.extract(r'\(([^)]+)\)')
#
#         # Create mask and filter the df
#         df_b_mask = pas_ward["BOROUGHNEIGHBOURHOOD;1"] == borough
#         df_filtered = pas_ward[df_b_mask]
#
#         # Group data by date and unique response col and count freq
#         grouped = df_filtered.groupby(["MONTH_YEAR", questions]).size().unstack(fill_value=0)
#
#         # Convert index to datetime
#         grouped.index = pd.to_datetime(grouped.index)
#
#         # Format the datetime index to "month year"
#         grouped.index = grouped.index.strftime('%b %Y')
#
#         # Plot stacked bar
#         try:
#             grouped.plot(kind='bar', stacked=True, figsize=(10, 7))
#
#             # Set labels
#             plt.xlabel('Date')
#             plt.ylabel('Frequency')
#
#             index = int(questions.split(";")[1])
#             question_content = question_dictionary["Question Content"][index]
#             plt.title(f'Frequency: {borough.strip()} {question_content}')
#             plt.legend(title='Responses', bbox_to_anchor=(1.05, 1), loc='upper left')
#             plt.xticks(rotation=45)
#             plt.tight_layout()
#
#             # Show plot
#             name = borough.strip().replace("/","-")
#             plt.savefig(f"data/savedgraphs/{name}_{questions}")
#         except:
#             name = borough.strip().replace("/", "-")
#             print(f"Nothing to plot:{name}, {borough},{questions}")
