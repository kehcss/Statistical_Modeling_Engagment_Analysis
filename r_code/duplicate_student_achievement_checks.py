import pandas as pd
import ast
import numpy as np

# Load the CSV files
duplicate_df = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\duplicate_Student_Achievement.csv')
summary_df = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\student_talkmove_summary_with_dorminat_details_file_merged.csv')

duplicate_df['student_ID'] = duplicate_df['student_ID'].astype(str)
summary_df['student_ID'] = summary_df['student_ID'].astype(str)

# Specify the columns to keep from the summary CSV
columns_to_keep = ['student_ID', 'session_IDs', 'unique_session_IDs_count', 
                   'unique_tutor_id_received_talkmove_count', 'tutor_id_received_talkmove', 'unique_tutor_percentage', 'dominate_tutor_id']

# Filter the summary DataFrame
summary_df_filtered = summary_df[columns_to_keep]

# Merge the DataFrames on 'student_ID'
merged_df = pd.merge(duplicate_df, summary_df_filtered, on='student_ID', how='left')

# Function to check if there are multiple IDs in the column
def count_ids(id_list):
    # Convert string representation of list to actual list if necessary
    if isinstance(id_list, str):
        # Remove the brackets and split by comma, strip spaces, and filter empty strings
        id_list = [x.strip() for x in id_list.strip('[]').split(',') if x.strip()]
    # Return 1 if more than one unique ID, 0 otherwise
    return 1 if len(set(id_list)) > 1 else 0

# Apply the function to the 'coach_ID' column
merged_df['multiple_coach'] = merged_df['coach_ID'].apply(count_ids)

# Apply the function to the 'Tutor_ID' column
merged_df['multiple_tutor'] = merged_df['tutor_ID'].apply(count_ids)


# Function to check presence and absence of tutor IDs
def analyze_tutor_ids(row):
    try:
        # Ensure Tutor_ID is a set of strings
        tutor_ids = {str(id) for id in ast.literal_eval(row['tutor_ID'])} if isinstance(row['tutor_ID'], str) else {str(id) for id in row['tutor_ID']}

        # Flatten the list of lists from tutor_id_received_talkmove, converting items to string for consistency
        if pd.isna(row['tutor_id_received_talkmove']):
            received_talkmove_ids = set()
        else:
            talkmove_list = ast.literal_eval(row['tutor_id_received_talkmove']) if isinstance(row['tutor_id_received_talkmove'], str) else row['tutor_id_received_talkmove']
            if isinstance(talkmove_list, list):
                received_talkmove_ids = {str(item) for sublist in talkmove_list for item in sublist if isinstance(sublist, list)}
            else:
                received_talkmove_ids = set()
    except (ValueError, SyntaxError):
        tutor_ids = set()
        received_talkmove_ids = set()

    in_talkmove = set()
    not_in_talkmove = set()

    # Compare IDs for presence or absence
    for tutor_id in tutor_ids:
        if tutor_id in received_talkmove_ids:
            in_talkmove.add(tutor_id)
        else:
            not_in_talkmove.add(tutor_id)

    # Convert sets to strings, return empty string if set is empty
    not_in_talkmove_str = str(not_in_talkmove) if not_in_talkmove else ""
    in_talkmove_str = str(in_talkmove) if in_talkmove else ""

    return pd.Series([not_in_talkmove_str, in_talkmove_str])


# Apply the function and create new columns
merged_df[['tutor_not_in_talkmove', 'tutor_in_talkmove']] = merged_df.apply(analyze_tutor_ids, axis=1)

# Define a filter condition where both columns have values or only 'tutor_not_in_talkmove' has a value
# Adding the new column based on the specified conditions
merged_df['one_or_more_tutor_not_in_talkmove'] = np.where(
    ((merged_df['tutor_not_in_talkmove'] != "") & (merged_df['tutor_in_talkmove'] != "")) |
    ((merged_df['tutor_not_in_talkmove'] != "") & (merged_df['tutor_in_talkmove'] == "")),
    1,
    0
)



# Adding the 'not_in_talkmove_dataset' column based on whether 'unique_session_IDs_count' is empty
merged_df['not_in_talkmove_dataset'] = np.where(
    merged_df['unique_session_IDs_count'].isna() | (merged_df['unique_session_IDs_count'] == ""),  # Checking if empty or NaN
    1,
    0
)



# Save the merged DataFrame to a new CSV file
merged_df.to_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\2_duplicate_student_achievement_details.csv', index=False)