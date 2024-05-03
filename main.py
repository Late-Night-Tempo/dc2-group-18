# Imports
import pandas as pd
# Including as an import to remember to place it in requirements.txt
import openpyxl

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# To read an excel file, install the optional dependency openpyxl. I personally converted to CSV using excel.
pas_data_borough = pd.read_csv("data/PAS_T&Cdashboard_to Q3 23-24 BOROUGH.csv")
pas_data_MPS = pd.read_csv("data/PAS_T&Cdashboard_to Q3 23-24 MPS.csv")

# Set datatypes BOROUGH
pas_data_borough = pas_data_borough.drop(columns=["Unnamed: 6", "Unnamed: 7", "Unnamed: 8", "Unnamed: 9"])
pd.to_datetime(pas_data_borough['Date'])
pas_data_borough = pas_data_borough.astype({'Survey': 'str', 'Borough': 'str', 'Measure': 'str'})
pas_data_borough.dropna(inplace=True)


# Set datatypes MPS
pd.to_datetime(pas_data_MPS['Date'])
pas_data_MPS = pas_data_MPS.astype({'Survey': 'str', 'Borough': 'str', 'Measure': 'str'})
pas_data_MPS.dropna(inplace=True)


# print check
# print(pas_data_borough)
# print(pas_data_MPS)

# plot things per borough over time to see any patterns...
for boroughs in pas_data_borough["Borough"].unique():
    for measures in pas_data_borough["Measure"].unique():
        cust_df_mask = pas_data_borough["Borough"] == boroughs
        cust_df = pas_data_borough[cust_df_mask]

        cust_df_meas_mask = cust_df["Measure"] == measures
        cust_df = cust_df[cust_df_meas_mask]

        x_cat = "Date"
        y_cat = "Proportion"


        checkplot = plt.plot(cust_df[x_cat], cust_df[y_cat], label=measures)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.legend(loc='upper left', bbox_to_anchor=(1.1, 1))
        plt.gcf().set_size_inches(8, 5)

    plt.title(f"{boroughs} {y_cat} Data")
    plt.show()



# Adjusted code from Visualization, as a dash may be a nice way to visualize the data later....
# import plotly.express as px
# from dash.dependencies import Input, Output
# import dash
# from dash import Dash, dcc, html
# import dash_bootstrap_components as dbc
#
# app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.ZEPHYR])
#
# # Customize Layout
# app.layout = dbc.Container([
#     # header
#     dcc.Markdown("Basic EDA", style={'fontSize': 45, 'textAlign': 'center'}),
#
# ], fluid=True)
#
# # Run App
# if __name__ == '__main__':
#     app.run_server(port=8051, debug=True, use_reloader=False)
