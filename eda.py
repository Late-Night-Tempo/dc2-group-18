import numpy as np
import pandas as pd
import openpyxl
import pyreadstat
from os import listdir
import geopandas as gpd
from shapely.geometry import Point
from tqdm import tqdm
import matplotlib.pyplot as plt

## Doing preliminary tests on 1 crime dataset...
#
#
# crime_data_df = pd.read_csv("data/CrimeDataMET/2021-04/2021-04-metropolitan-street.csv")
#
# # Info prints
# print(".INFO")
# print(crime_data_df.info())
#
# print("COLUMNS")
# print(crime_data_df.columns)
#
# print("BASIC PRINT")
# print(crime_data_df)
#
# print("NAN COUNT")
# print(crime_data_df.isnull().sum(axis=0))
#
# print("DUPLICATE ROW COUNT")
# print(len(crime_data_df)-len(crime_data_df.drop_duplicates()))
#
# print("CRIME TYPE UNIQUE")
# print(crime_data_df["Crime type"].unique())
#
# print("LAST OUTCOME CATEGORY UNIQUE")
# print(crime_data_df["Last outcome category"].unique())
#
# print("END OF TEST RUN. BEGIN DATA MERGE.")
#
# # Dataframes to hold all data
# street_df = pd.DataFrame()
# search_df = pd.DataFrame()
#
# # Collect all folders
# all_csv_folders = listdir("data/CrimeDataMET")
#
# # Per folder, get csvs inside and add them to their respective dataframes
# for folders in all_csv_folders:
#     csv_file_names = listdir("data/CrimeDataMET/" + folders)
#
#     street_data =["data/CrimeDataMET/" + folders + "/" + fname for fname in csv_file_names if fname.endswith("street.csv")]
#     search_data = ["data/CrimeDataMET/" + folders + "/" + fname for fname in csv_file_names if fname.endswith("search.csv")]
#
#
#     # We know the database only holds one of each per month, so we hardcode it
#     add_street = pd.read_csv(street_data[0])
#     add_search = pd.read_csv(search_data[0])
#
#     street_df = pd.concat([street_df, add_street])
#     search_df = pd.concat([search_df, add_search])
#
#
# print(street_df)
# print(search_df)
#
# street_df.to_csv("RawStreetData.csv")
# search_df.to_csv("RawSearchData.csv")


# Clean the raw csv data...
street_df = pd.read_csv("data/RawStreetData.csv")
search_df = pd.read_csv("data/RawSearchData.csv")

#Print pre-clean lengths
# print(len(street_df))
# print(len(search_df))

#Print columns per df
# print(street_df.columns)
# print(search_df.columns)

# Drop unintentional index column
street_df.drop(columns=["Unnamed: 0"], inplace=True)
search_df.drop(columns=["Unnamed: 0"], inplace=True)

# Remove duplicates from both
street_df.drop_duplicates(inplace=True)
search_df.drop_duplicates(inplace=True)

#Print post-dup drop lengths
# print(len(street_df))
# print(len(search_df))

# Remove no location / nan lat/longitudes
street_df.dropna(subset=["Latitude", "Longitude"], inplace=True)
search_df.dropna(subset=["Latitude", "Longitude"], inplace=True)

# print(len(street_df))
# print(len(search_df))

print("BEGIN COLUMN AUTO DROP")

for items in street_df.columns:
    if len(street_df[items].unique()) == 1:
        street_df.drop(columns=[items], inplace=True)
    else:
        pass
        #print(street_df[items].unique())

for items in search_df.columns:
    if len(search_df[items].unique()) == 1:
        search_df.drop(columns=[items], inplace=True)
    else:
        pass
        #print(search_df[items].unique())

print("BEGIN MAPPING")

## Begin finding borough location

# Collect map
map_path = "data/London-wards-2018/London-wards-2018_ESRI/London_Ward_CityMerged.shp"
gdf = gpd.read_file(map_path)

# Convert to coordinates
gdf.to_crs(epsg=4326, inplace=True)

# Get all points as a list!!!
street_points = []
search_points = []

print("COLLECT LONG LAT - STREET DATA")
for point_index, point_rows in tqdm(street_df.iterrows(), total=len(street_df)):
    point = Point(point_rows["Longitude"], point_rows["Latitude"])
    street_points.append(point)

print("COLLECT LONG LAT - SEARCH DATA")
for point_index, point_rows in tqdm(search_df.iterrows(), total=len(search_df)):
    point = Point(point_rows["Longitude"], point_rows["Latitude"])
    search_points.append(point)

street_points = gpd.GeoDataFrame(geometry=street_points, crs=gdf.crs)
search_points = gpd.GeoDataFrame(geometry=search_points, crs=gdf.crs)



# Do a join to get borough names

# Joins the points and districts together, then creates dataframe from it
street_districts = pd.DataFrame(gpd.sjoin(street_points, gdf, how="left", op="within"))
search_districts = pd.DataFrame(gpd.sjoin(search_points, gdf, how="left", op="within"))

# Add only borough column to the street df
street_df["Borough"] = street_districts["DISTRICT"]
search_df["Borough"] = search_districts["DISTRICT"]

print(street_df.info())
print(search_df.info())

street_df.dropna(subset=["Borough"], inplace=True)
search_df.dropna(subset=["Borough"], inplace=True)

street_df["Borough"] = street_df["Borough"].str.lower()
search_df["Borough"] = search_df["Borough"].str.lower()

print(street_df["Borough"].unique())
print(search_df["Borough"].unique())


street_df.to_csv("CleanStreetData.csv", index=False)
search_df.to_csv("CleanSearchData.csv", index=False)