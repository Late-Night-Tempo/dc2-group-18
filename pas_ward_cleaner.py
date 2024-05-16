import numpy as np
import pandas as pd
import openpyxl
import pyreadstat
from os import listdir
import geopandas as gpd
from shapely.geometry import Point
from tqdm import tqdm
import matplotlib.pyplot as plt


# Collect all csvs from pas ward data
csv_file_names = listdir("data/pas_data_ward_level")
search_data = ["data/pas_data_ward_level" + "/" + fname for fname in csv_file_names if fname.endswith(".csv")]

# Take CSVs and make raw dataset
raw_pas_df = pd.DataFrame()

for csvfiles in search_data:
    raw_partial_df = pd.read_csv(csvfiles)
    raw_pas_df = pd.concat([raw_pas_df, raw_partial_df])

# Convert interview date to datetime
pd.to_datetime(raw_pas_df['interview_date'])

#raw_pas_df.isnull().sum(axis=0)

# Save raw as csv
raw_pas_df.to_csv("RawPasWardData.csv")

#print(raw_pas_df.columns)
print("PRE AND POST AUTO DROP COlS")
total_pas_len = len(raw_pas_df)
print(len(raw_pas_df.columns))



# Begin iterating through dictionary
for cols in raw_pas_df:
    # How many have responded to the question
    percentage_that_col = 100 - (raw_pas_df[cols].isnull().sum() / len(raw_pas_df) * 100)
    print(f"COL QUESTION: {cols}, PERCENT ANS: {percentage_that_col}")


    # Drop any columns without unique values at all
    if len(raw_pas_df[cols].unique()) == 1:
        raw_pas_df.drop(columns=[cols], inplace=True)


# Open the text file
with open('data/PAS_data_dictionaries_shared/PAS_Sharing_EXTERNAL_data dictionary_1517.txt', 'r') as file:
    # Read the lines of the file
    lines = file.readlines()

    # Set question label
    current_topic= "Default topic"

    # Create dataframe for outgoing excel file
    pd_excel = pd.DataFrame()
    question_list = []
    question_label_list = []

    # Parse each line based on newlines
    for line in lines:
        # Split the line into fields based on newlines
        fields = line.split('\n')
        # Process each field by tabs

        for field in fields:
            # Split again on tabs
            internal_data = field.split("\t")

            # Check if we have hit a question
            if internal_data[0] in raw_pas_df.columns:
                current_topic = internal_data[0]
                print(f"Main value: {internal_data[0]}")
            else:
                # print any subvalues
                print(f"Subvalues of {current_topic}: {internal_data}")
                # If label is present, then question comes next. Save questions.
                if "Label" in internal_data:
                    question = internal_data.index("Label")

                    # Add to storage
                    question_list.append(internal_data[question + 1])
                    question_label_list.append(current_topic)


    # Store questions data
    question_percents = []
    question_absolute = []

    question_label_stored = []
    question_stored = []

    # Go through dataframe again so that we get only the values which actually show up in both.
    # Otherwise I've been getting length errors and this was the easiest way to deal with that.

    for cols in raw_pas_df:
        if cols in question_label_list:
            abs_that_col = len(raw_pas_df) - raw_pas_df[cols].isnull().sum()
            percentage_that_col = 100 - (raw_pas_df[cols].isnull().sum() / len(raw_pas_df) * 100)

            # Save response counts
            question_absolute.append(abs_that_col)
            question_percents.append(percentage_that_col)

            # Save question label and the question asked
            question_label_stored.append(cols)
            question_stored.append(question_list[question_label_list.index(cols)])



    # Implement stored data into dataframe
    pd_excel["Question Label"] = question_label_stored
    pd_excel["Question Content"] = question_stored

    pd_excel["Absolute Responses"] = question_absolute
    pd_excel["Percentage Responses"] = question_percents
    pd_excel["Keep Bool"] = True

    print(pd_excel)
    pd_excel.to_excel("TrueFalseSetter.xlsx")

