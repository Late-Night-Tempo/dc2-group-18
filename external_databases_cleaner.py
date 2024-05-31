import pandas as pd

# Adding import of optional dependency to auto-sync requirements, as it is needed for .xls files
import xlrd



# Use inactivity + earning below LLW, and GCSE


# Begin cleaning inactivity. Choosing to ignore gender for now.

# Collect all data
inactivity_df = pd.read_csv("data/External Databases/economic-inactivity.csv")

# Remove rows with not-boroughs
# Let it be known that I've changed "City of Westminster" to just "Westminster" as while there is a distinction it appears to be somewhat vague
london_boroughs_list = ["Westminster", "Kensington and Chelsea", "Hammersmith and Fulham", "Wandsworth", "Lambeth", "Southwark",
    "Tower Hamlets", "Hackney", "Islington", "Camden", "Brent", "Ealing", "Hounslow", "Richmond upon Thames",
    "Kingston upon Thames", "Merton", "Sutton", "Croydon", "Bromley", "Lewisham", "Greenwich", "Bexley", "Havering",
    "Barking and Dagenham", "Redbridge", "Newham", "Waltham Forest", "Haringey", "Enfield", "Barnet", "Harrow",
    "Hillingdon"]


# honestly this .csv is wonderful it doesn't really need any particular changes. The columns are named nicely, datapoints full, its pretty great!
# No nulls either, I'm very impressed. Still saving this as a new csv for the sake of it though.
for index, row in enumerate(inactivity_df["Area"]):
    if row not in london_boroughs_list:
        inactivity_df.drop(index=index, axis=1, inplace=True)

inactivity_df.to_csv("CleanedInactivityData.csv")




# Clean below LLW by borough

# Read excel file, using the Number sheet
below_llw_df = pd.read_excel("data/External Databases/employees-earning-below-llw-borough.xls", sheet_name="Number")



# Drop empty nan column which separates the numbers from the confidence intervals actually nvm we don't need the
# confidence intervals... Also, I did a bit of cleaning by hand directly in the xls file. The column issues are just
# awful, so do note this requires a little tweaking but if we don't have to make this reproducible it should be fine
columns_drop = [name for name in below_llw_df.columns if "+" in str(name)]
below_llw_df.drop(columns=["Unnamed: 20"], inplace=True)
below_llw_df.drop(columns=columns_drop, inplace=True)


# If it's not in the boroughs list, drop it
for index, row in enumerate(below_llw_df["Area Name"]):
    if index > 1 and row not in london_boroughs_list:
        below_llw_df.drop(index=index, axis=1, inplace=True)

# Concatenate column names with the values in the first row
below_llw_df.columns = [
    f"{col}_{val}" if not pd.isna(val) else col
    for col, val in zip(below_llw_df.columns, below_llw_df.iloc[0])
]
# Drop the first row
below_llw_df = below_llw_df.drop(index=0)

# Reset the index
below_llw_df.reset_index(drop=True, inplace=True)

# Get rid of extra space row
below_llw_df.drop(index=0, axis=0, inplace=True)

# # test prints
# print(below_llw_df.columns)
# print(below_llw_df.head())

# save dataset

below_llw_df.to_csv("CleanedBelowLLWBorough.csv")



#
#
#
# Clean GCSE.... Pick one database to use. need to merge sheets...........

# # Get the file
# file = pd.ExcelFile("data/External Databases/GCSE results by ethnicity.xlsx")
#
# # Get all sheet names
# names = file.sheet_names
#
# # Remove metadata sheet
# names = names[1:]
#
# # Concatenate all data together into one large dataframe
# gcse_ethnicity_df = pd.concat([file.parse(name) for name in names])
#
# # Test print
# print(gcse_ethnicity_df)