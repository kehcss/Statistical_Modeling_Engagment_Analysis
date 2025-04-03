import pandas as pd

# Load the data from CSV files
student_achievement = pd.read_excel(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\student_id_not_found_in_achievement.xlsx')
student_survey = pd.read_excel(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\Student_id_not_found_in_survey.xlsx')

# Define the columns to be included from both files (if available)
common_columns = ['student_ID', 'session_IDs', 'unique_session_IDs_count', 'tutor_id_received_talkmove', 'dominate_tutor_id']

# Filter the dataframes to include only the relevant columns
student_achievement_filtered = student_achievement[common_columns]
student_survey_filtered = student_survey[common_columns]

# Perform an outer join on the 'student_ID' column
combined_df = pd.merge(student_achievement_filtered, student_survey_filtered, on='student_ID', how='outer', suffixes=('_ach', '_sur'))

# Ensure the proper selection of columns without future warning
for column in common_columns[1:]:  # Skip 'student_ID' as it's the key for joining
    ach_column = column + '_ach'
    sur_column = column + '_sur'
    combined_df[column] = combined_df[ach_column].where(combined_df[ach_column].notna(), combined_df[sur_column])

# Convert the student IDs to sets for efficient lookup
achievement_ids = set(student_achievement['student_ID'])
survey_ids = set(student_survey['student_ID'])

# Add 'missing_achievement' and 'missing_survey' columns by checking the presence of student_ID in original dataframes
combined_df['missing_achievement'] = combined_df['student_ID'].apply(lambda x: 1 if x in achievement_ids else 0)
combined_df['missing_survey'] = combined_df['student_ID'].apply(lambda x: 1 if x in survey_ids else 0)

# Drop the temporary columns used during merging
combined_df.drop([col for col in combined_df.columns if col.endswith(('_ach', '_sur'))], axis=1, inplace=True)


# Load the new CSV files
currated_FSA = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\curated-FSA - curated-FSA-updated.csv')
currate_STAR = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\curated-STAR - curated-STAR-updated.csv')

# Make sure the student_ID is consistently formatted across all datasets
# Assuming student_ID needs to be a string, adjust as necessary
combined_df['student_ID'] = combined_df['student_ID'].astype(str)
currated_FSA['student_ID'] = currated_FSA['student_ID'].astype(str)
currate_STAR['student_ID'] = currate_STAR['student_ID'].astype(str)

# Convert the student IDs in the new files to sets for efficient lookup
FSA_ids = set(currated_FSA['student_ID'])
STAR_ids = set(currate_STAR['student_ID'])

# Add 'found_in_STAR' and 'found_in_FSA' columns by checking the presence of student_ID in the new dataframes
combined_df['found_in_STAR'] = combined_df['student_ID'].apply(lambda x: 1 if x in STAR_ids else 0)
combined_df['found_in_FSA'] = combined_df['student_ID'].apply(lambda x: 1 if x in FSA_ids else 0)

# Update 'missing_achievement' where 'found_in_FSA' or 'found_in_STAR' is 1
combined_df.loc[(combined_df['found_in_FSA'] == 1) | (combined_df['found_in_STAR'] == 1), 'missing_achievement'] = 0

# # Filter the DataFrame to include only cases where 'missing_achievement' or 'missing_survey' equals 1
# combined_df = combined_df[(combined_df['missing_achievement'] == 1) | (combined_df['missing_survey'] == 1)]


#Load other CSV file
user_missing_region = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\Tutor, SD and Site IDs - Users with missing region.csv')
site_director = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\Tutor, SD and Site IDs - Site Director List.csv')
tutor_list = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\Tutor, SD and Site IDs - Tutor List.csv')

# Assuming student_ID needs to be a string, adjust as necessary
combined_df['student_ID'] = combined_df['student_ID'].astype(str)
user_missing_region['student_ID'] = user_missing_region['ID'].astype(str)
site_director['student_ID'] = site_director['site director ID'].astype(str)
tutor_list['student_ID'] = tutor_list['tutor ID'].astype(str)

# Create sets for efficient lookup
user_missing_region_ids = set(user_missing_region['student_ID'])
site_director_ids = set(site_director['student_ID'])
tutor_list_ids = set(tutor_list['student_ID'])

# Add columns by checking the presence of student_ID in the additional dataframes
combined_df['user_missing_region'] = combined_df['student_ID'].apply(lambda x: 1 if x in user_missing_region_ids else 0)
combined_df['site_director'] = combined_df['student_ID'].apply(lambda x: 1 if x in site_director_ids else 0)
combined_df['tutor_list'] = combined_df['student_ID'].apply(lambda x: 1 if x in tutor_list_ids else 0)


summary_df = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\student_talkmove_summary_with_dorminat_details_file_merged.csv')
# Filter the DataFrame to include only cases where 'missing_achievement' or 'missing_survey' equals 1
summary_df = summary_df[(summary_df['found_in_saga_crosswalk'] == 1) | (summary_df['found_in_duplicate_saga_crosswalk'] == 1)]

# Make sure the student_ID is consistently formatted across all datasets
# Assuming student_ID needs to be a string, adjust as necessary
combined_df['student_ID'] = combined_df['student_ID'].astype(str)
summary_df['student_ID'] = summary_df['student_ID'].astype(str)

# Convert the student IDs in the new files to sets for efficient lookup
summary_ids = set(summary_df['student_ID'])


# Add 'found_in_STAR' and 'found_in_FSA' columns by checking the presence of student_ID in the new dataframes
combined_df['has_anon_student_ID'] = combined_df['student_ID'].apply(lambda x: 1 if x in summary_ids else 0)


# Save the combined dataframe to an Excel file
combined_df.to_excel(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\4_updated_combined_missing_student_ids.xlsx', index=True)