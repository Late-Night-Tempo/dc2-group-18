import pandas as pd


pas_tf_cols_df = pd.read_excel("data/TrueFalsePasReducer.xlsx")
pas_data_df = pd.read_csv("data/RawPasWardData.csv")

print(pas_data_df)

# Find columns that match
# if match, drop.


#
# for cols in pas_data_df.columns:
#     if cols in pas_tf_cols_df["Question Label"]:
#         print("present:", cols)
#
#



for col in pas_data_df.columns:
    if col in list(pas_tf_cols_df["Question Label"]):
        # Find the index where the column matches
        index_series = pas_tf_cols_df[pas_tf_cols_df["Question Label"] == col].index

        # Ensure we only have one match
        if len(index_series) == 1:
            index = index_series[0]
            # Get the boolean value for "Keep Bool"
            keep_bool = pas_tf_cols_df.loc[index, "Keep Bool"]
            if keep_bool:
                # Rename the column by appending the corresponding "Question Content" value
                question_content = pas_tf_cols_df.loc[index, "Question Content"]
                new_col_name = f"{col};{index}"
                pas_data_df.rename(columns={col: new_col_name}, inplace=True)
            else:
                # Drop the column if keep_bool is False
                try:
                    pas_data_df.drop(col, axis=1, inplace=True)
                except KeyError as e:
                    print(f"Column '{col}' not found: {e}")

        else:
            print(f"Multiple or no matches found for column '{col}' in 'Question Label'.")


# List to store columns to drop
col_drop = []

# Iterate over the columns starting from index 5 (i.e., the 6th column)
for i, col in enumerate(pas_data_df.columns):
    if i > 15 and ';' not in col:
        col_drop.append(col)

# Drop the collected columns
pas_data_df.drop(columns=col_drop, inplace=True)

print(pas_data_df)
pas_data_df.to_csv("CleanedDroppedPasWardData2.csv", index=False)

