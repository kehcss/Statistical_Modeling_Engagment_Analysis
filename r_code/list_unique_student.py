import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\Student_Achievement_Intercept_Slope_04_12_2025.csv')

# #
filtered_df = df

# # Filter the DataFrame for rows where 'is_in_achievement' is 1 (assuming it's already correctly set as numeric)
# filtered_df = df[df['is_in_achievement'] == 1]

# filtered_df = filtered_df[filtered_df['unique_session_IDs_count'] > 4]

# # # Further filter to exclude rows where 'coach_ID' is NaN or blank (empty strings)
# # filtered_df = filtered_df[filtered_df['coach_ID'].notna()]




# Get the unique speaker_ids
unique_speaker_ids = filtered_df['student_ID'].unique()

# Create a DataFrame with the unique speaker_ids
unique_speaker_ids_df = pd.DataFrame(unique_speaker_ids, columns=['student_ID'])

# Display the DataFrame
print(unique_speaker_ids_df)
