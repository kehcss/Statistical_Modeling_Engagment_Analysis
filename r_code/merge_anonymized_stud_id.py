# import pandas as pd

# # Function 1: Merge Bobby CSV and Sandra's ID Analyumnous ID Excel file and return updated CSV
# def merge_files_and_update_student_id(csv_file_path, excel_file_path):
#     # Load the CSV and Excel files into DataFrames
#     csv_df = pd.read_csv(csv_file_path)
#     excel_df = pd.read_excel(excel_file_path)

#     # Add a new column 'New Student ID' based on matching 'speaker' and 'Saga Student ID'
#     csv_df['New Student ID'] = csv_df['speaker'].map(
#         dict(zip(excel_df['Saga Student ID'], excel_df['Anonymized student ID']))
#     )

#     # Convert 'New Student ID' to string to ensure consistent type for merging
#     csv_df['New Student ID'] = csv_df['New Student ID'].astype(str)
    
#     # Return the updated DataFrame
#     return csv_df

# # Function 2: Merge two CSV files and return the final merged file
# def merge_and_save_final_csv(updated_df, csv2_path):
#     # Load the second CSV file
#     data2 = pd.read_csv(csv2_path)
    
#     # Convert 'student_ID' in data2 to string to ensure consistent type for merging
#     data2['student_ID'] = data2['student_ID'].astype(str)

#     # Perform the inner join (merge)
#     merged_data = pd.merge(updated_df, data2, left_on='New Student ID', right_on='student_ID', how='inner')

#     # Save the merged result to a CSV file and return the path
#     final_csv_file_path = csv2_path.replace(".csv", "_final_merged.csv")
#     merged_data.to_csv(final_csv_file_path, index=False)

#     print(f"Final merged CSV file saved as: {final_csv_file_path}")
#     return final_csv_file_path

# # Example usage:
# # Example usage:
# csv_file_path = r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\speaker-utterances-2023-08-01-to-2024-06-14.csv'
# excel_file_path = r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\2024 Saga Crosswalk - Student IDs.xlsx'
# csv2_path = r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\Student_Achievement_Intercept_Slope_10_23_2024.csv'
# # Step 1: Merge CSV and Excel to update the student IDs
# updated_df = merge_files_and_update_student_id(csv_file_path, excel_file_path)

# # Step 2: Use the updated DataFrame and merge it with the second CSV file, then save the final CSV
# final_csv_file = merge_and_save_final_csv(updated_df, csv2_path)




import pandas as pd
from collections import defaultdict

# def merge_slope_intercept(uttrance_file: str, slopes_file: str, output_file: str):
#     """
#     Merges slope and intercept from the slopes file to the uttrance file where speaker_type is 'student',
#     and orders the final DataFrame according to an index column.
#     """
#     uttrance_df = pd.read_csv(uttrance_file)
#     slopes_df = pd.read_csv(slopes_file)

#     uttrance_df['index_col'] = range(len(uttrance_df))
#     uttrance_df['speaker'] = uttrance_df['speaker'].astype(str)
#     slopes_df['student_ID'] = slopes_df['student_ID'].astype(str)

#     student_uttrance_df = uttrance_df[uttrance_df['speaker_type'] == 'student']
#     merged_student_df = student_uttrance_df.merge(
#         slopes_df[['student_ID', 'Slope', 'Intercept']],
#         left_on='speaker',
#         right_on='student_ID',
#         how='left'
#     )
#     merged_student_df.drop(columns=['student_ID'], inplace=True)
#     final_df = pd.concat([merged_student_df, uttrance_df[uttrance_df['speaker_type'] != 'student']], ignore_index=True)
#     final_df = final_df.sort_values('index_col').drop(columns=['index_col'])
#     final_df.to_csv(output_file, index=False)

#     print(f"Merged file saved as '{output_file}'.")
#     return final_df


# def preprocess_data(df: pd.DataFrame, output_file: str):
#     """
#     Preprocesses the DataFrame by filtering out rows where 'Slope' is NaN and 'language' is not 'en'.
#     """
#     initial_count = len(df)
#     df_slope_filtered = df[~((df['speaker_type'] == 'student') & (df['Slope'].isna()))]
#     slope_filtered_count = initial_count - len(df_slope_filtered)
#     print(f"Number of rows filtered out where 'speaker_type' is 'student' and 'Slope' is NaN: {slope_filtered_count}")

#     df_language_filtered = df_slope_filtered[df_slope_filtered['language'] == 'en']
#     language_filtered_count = len(df_slope_filtered) - len(df_language_filtered)
#     print(f"Number of rows filtered out where 'language' is not 'en': {language_filtered_count}")

#     df_language_filtered.to_csv(output_file, index=False)
#     print(f"Preprocessed file saved as '{output_file}'.")
#     return df_language_filtered


# def add_usual_student_group(df: pd.DataFrame, output_file: str):
#     """
#     Adds a 'usual_student_group' column to the DataFrame indicating the largest group combination for each student ID.
#     """
#     # Dictionary to track each student's groups and their sizes
#     student_groups = defaultdict(lambda: defaultdict(int))

#     # Calculate group counts and assign to each student ID
#     for ids in df['student_IDs'].dropna():  # Skip NaN values
#         id_group = ";".join(sorted(ids.split(";")))
#         for student_id in id_group.split(";"):
#             student_groups[student_id][id_group] = max(student_groups[student_id][id_group], len(id_group.split(";")))

#     # Determine the usual group for each student
#     usual_group_mapping = {}
#     for student_id, groups in student_groups.items():
#         usual_group = max(groups, key=lambda g: (groups[g], g))
#         usual_group_mapping[student_id] = usual_group

#     # Function to map the 'usual group' for each row's student IDs, handling NaN values
#     def map_usual_group(ids):
#         if pd.isna(ids):  # Check if the value is NaN
#             return None
#         first_student_id = ids.split(";")[0]
#         return usual_group_mapping.get(first_student_id, ids)

#     # Apply the function to create a new column 'usual_student_group'
#     df['usual_student_group'] = df['student_IDs'].apply(map_usual_group)

#     # Save the final DataFrame to the specified output file
#     df.to_csv(output_file, index=False)
#     print(f"File with 'usual_student_group' column saved as '{output_file}'.")
#     return df

# # Example usage
# merged_df = merge_slope_intercept(
#     uttrance_file=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\speaker-utterances-2023-08-01-to-2024-06-14.csv',
#     slopes_file=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\Student_Achievement_Intercept_Slope_10_23_2024.csv',
#     output_file=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\final.csv'
# )

# preprocessed_df = preprocess_data(
#     df=merged_df,
#     output_file=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\preprocessed_final.csv'
# )

# # Adding 'usual_student_group' to the preprocessed data
# final_with_usual_group_df = add_usual_student_group(
#     df=preprocessed_df,
#     output_file=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\final_with_usual_group.csv'
# )



#MERGE data from chat and speech, AND Calculate talkmove, uttrance ratio

# # Load the CSV file
# df = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\speaker-utterances-2023-08-01-to-2024-06-14.csv')

# # Filter for rows where language is 'en'
# df = df[df['language'] == 'en']

# # Columns to sum
# columns_to_sum = [
#     'utterance_count', 'learning_community_count', 'rigorous_thinking_count', 
#     'content_knowledge_count', 'tutor_keeping_together_count', 'tutor_students_relating_count', 
#     'tutor_restating_count', 'tutor_revoicing_count', 'tutor_reasoning_count', 'tutor_accuracy_count', 
#     'student_relating_count', 'student_asking_for_info_count', 'student_making_claim_count', 
#     'student_providing_evidence_count', 'talk_move_count'
# ]

# # Columns to average (take the mean)
# columns_to_mean = ['asr_confidence_mean', 'talk_move_probability_mean']

# # Define a function to apply sum and mean appropriately
# def process_group(group):
#     if group['mode'].nunique() > 1:
#         # Sum the specified columns
#         summed_data = group[columns_to_sum].sum().to_frame().T
        
#         # Calculate the mean for specified columns
#         mean_data = group[columns_to_mean].mean().to_frame().T
        
#         # Combine summed and mean data
#         combined_data = pd.concat([summed_data, mean_data], axis=1)
        
#         # Set mode to 'both' for merged cases
#         combined_data['mode'] = 'both'
        
#         # Calculate talkmove_ratio as talk_move_count / utterance_count
#         combined_data['talkmove_ratio'] = combined_data['talk_move_count'] / combined_data['utterance_count']
        
#         # Keep other columns from the first entry
#         other_columns = group.iloc[0][[
#             'coach_ID', 'tutor_ID', 'region', 'student_IDs', 'session_ID', 
#             'session_date', 'session_time', 'session_length_mins', 
#             'speaker_type', 'speaker', 'language'
#         ]].to_frame().T
        
#         # Concatenate the other columns with the combined data
#         result = pd.concat([other_columns.reset_index(drop=True), combined_data.reset_index(drop=True)], axis=1)
#         return result
#     else:
#         # For cases where mode does not differ, just return the first row as it is and calculate talkmove_ratio
#         row = group.iloc[0].copy()
#         row['talkmove_ratio'] = row['talk_move_count'] / row['utterance_count'] if row['utterance_count'] != 0 else 0
#         return row.to_frame().T

# # Apply the function to each group of (speaker, session_ID)
# processed_df = df.groupby(['speaker', 'session_ID']).apply(process_group).reset_index(drop=True)

# # Save to a new CSV file
# processed_df.to_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\speaker-utterances-2023-08-01-to-2024-06-14_merged_mode.csv', index=False)

#DATA CHECK CODE
# def count_tutor_equals_speaker(file_path: str):
#     """
#     Reads a CSV file and counts cases where 'tutor_ID' is equal to 'speaker_ID' and 'speaker_type' is 'student'.
    
#     Args:
#     - file_path (str): The path to the CSV file (e.g., 'preprocessed_final.csv').
    
#     Returns:
#     - count (int): The number of cases that match the conditions.
#     """
#     # Load the CSV file
#     df = pd.read_csv(file_path)

#     # Filter rows where 'tutor_ID' == 'speaker_ID' and 'speaker_type' == 'student'
#     filtered_df = df[(df['tutor_ID'] == df['speaker']) & (df['speaker_type'] == 'student')]

#     # Count the number of matching cases
#     count = len(filtered_df)
#     print(f"Number of cases where 'tutor_ID' equals 'speaker_ID' and 'speaker_type' is 'student': {count}")
    
#     return count

# # Example usage
# count = count_tutor_equals_speaker(
#     file_path=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\final.csv'
# )

# def count_tutor_in_speaker_for_students(file_path: str):
#     """
#     Reads a CSV file and counts cases where an ID in the 'tutor_ID' column also appears in the 'speaker_ID' column
#     when 'speaker_type' is 'student'.
    
#     Args:
#     - file_path (str): The path to the CSV file (e.g., 'preprocessed_final.csv').
    
#     Returns:
#     - count (int): The number of cases where the ID in 'speaker_ID' exists in 'tutor_ID' for 'student' speaker_type.
#     """
#     # Load the CSV file
#     df = pd.read_csv(file_path)

#     # Get all unique IDs in the 'tutor_ID' column
#     tutor_ids = set(df['tutor_ID'].dropna().astype(str))

#     # Filter rows where 'speaker_type' is 'student' and 'speaker_ID' exists in tutor_ids
#     student_speaker_df = df[(df['speaker_type'] == 'student') & (df['speaker'].astype(str).isin(tutor_ids))]

#     # Count the number of matching cases
#     count = len(student_speaker_df)
#     print(f"Number of cases where 'speaker_ID' exists in 'tutor_ID' and 'speaker_type' is 'student': {count}")
    
#     return count

# # Example usage
# count = count_tutor_in_speaker_for_students(
#     file_path=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\preprocessed_final.csv'
# )





#Summarizing the datasets
# def summarize_talk_moves_with_merge_note(file_path: str, output_file: str):
#     """
#     Summarizes talk moves for each unique 'speaker_id' where 'speaker_type' is 'student'.
#     Produces a CSV file containing each unique 'speaker_id', a list of 'session_ID's,
#     a list of 'talk_move_count's per session, a column for total 'talk_move_count' sum,
#     and a 'merge_note' column for cases where session IDs were summed.
    
#     Args:
#     - file_path (str): The path to the input CSV file (e.g., 'preprocessed_final.csv').
#     - output_file (str): The path to save the summarized output CSV file.
    
#     Returns:
#     - summary_df (pd.DataFrame): The resulting DataFrame with summarized talk moves and merge notes.
#     """
#     # Load the CSV file
#     df = pd.read_csv(file_path)

#     # Filter for rows where 'speaker_type' is 'student'
#     student_df = df[df['speaker_type'] == 'student']

#     # Group by 'speaker_id' and aggregate data
#     summary_data = {
#         'speaker': [],
#         'session_IDs': [],
#         'talk_move_counts': [],
#         'total_talk_move_count': [],
#         'merge_note': []
#     }

#     for speaker, group in student_df.groupby('speaker'):
#         # Count occurrences of each session_ID
#         session_counts = group['session_ID'].value_counts()
#         duplicate_sessions = session_counts[session_counts > 1].index.tolist()
        
#         # Get unique session IDs and corresponding talk move counts
#         session_IDs = group['session_ID'].unique().tolist()
#         talk_move_counts = group.groupby('session_ID')['talk_move_count'].sum().tolist()
        
#         # Sum all talk move counts for the current speaker_id
#         total_talk_move_count = sum(talk_move_counts)
        
#         # Set merge note if there were any duplicate sessions
#         merge_note = "speech and chat summed" if duplicate_sessions else ""

#         # Append to the summary data
#         summary_data['speaker'].append(speaker)
#         summary_data['session_IDs'].append(session_IDs)
#         summary_data['talk_move_counts'].append(talk_move_counts)
#         summary_data['total_talk_move_count'].append(total_talk_move_count)
#         summary_data['merge_note'].append(merge_note)

#     # Create a DataFrame from the summary data
#     summary_df = pd.DataFrame(summary_data)

#     # Save the summary DataFrame to a new CSV file
#     summary_df.to_csv(output_file, index=False)
#     print(f"Summary file saved as '{output_file}'.")

#     return summary_df

# # Example usage
# summary_df = summarize_talk_moves_with_merge_note(
#     file_path=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\preprocessed_final.csv',
#     output_file=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\summary_talk_moves_with_recieved.csv'
#)


# def summarize_talk_moves_with_received_talkmove(file_path: str, output_file: str):
#     """
#     Summarizes talk moves for each unique 'speaker_id' where 'speaker_type' is 'student'.
#     Produces a CSV file containing each unique 'speaker_id', a list of 'session_ID's,
#     a list of 'talk_move_count's per session, a column for total 'talk_move_count' sum,
#     a 'merge_note' column for cases where session IDs were summed,
#     a 'received_student_talkmove' column for summed talk moves from other students,
#     a 'student_id_received_talkmove' column listing those student IDs,
#     and 'sum_received_student_talkmove' column for total received talk moves.
    
#     Args:
#     - file_path (str): The path to the input CSV file (e.g., 'preprocessed_final.csv').
#     - output_file (str): The path to save the summarized output CSV file.
    
#     Returns:
#     - summary_df (pd.DataFrame): The resulting DataFrame with summarized talk moves and merge notes.
#     """
#     # Load the CSV file
#     df = pd.read_csv(file_path)
    
#     # Filter for rows where 'speaker_type' is 'student'
#     english_df = df[df['language'] == 'en']

#     # Filter for rows where 'speaker_type' is 'student'
#     student_df = english_df[english_df['speaker_type'] == 'student']

#     # Group by 'speaker_id' and aggregate data
#     summary_data = {
#         'speaker': [],
#         'session_IDs': [],
#         'talk_move_counts': [],
#         'total_talk_move_count': [],
#         'merge_note': [],
#         'received_student_talkmove': [],
#         'student_id_received_talkmove': [],
#         'sum_received_student_talkmove': []
#     }

#     for speaker, group in student_df.groupby('speaker'):
#         # Count occurrences of each session_ID
#         session_counts = group['session_ID'].value_counts()
#         duplicate_sessions = session_counts[session_counts > 1].index.tolist()
        
#         # Get unique session IDs and corresponding talk move counts
#         session_IDs = group['session_ID'].unique().tolist()
#         talk_move_counts = group.groupby('session_ID')['talk_move_count'].sum().tolist()
        
#         # Sum all talk move counts for the current speaker
#         total_talk_move_count = sum(talk_move_counts)
        
#         # Set merge note if there were any duplicate sessions
#         merge_note = "speech and chat summed" if duplicate_sessions else ""

#         # Initialize lists to store received talk move counts and speaker IDs
#         received_talkmove_counts = []
#         received_speaker_ids = []

#         # Iterate through each unique session for this speaker
#         for session in session_IDs:
#             # Filter to get rows in this session where speaker is not the current speaker
#             other_speakers_in_session = student_df[
#                 (student_df['session_ID'] == session) &
#                 (student_df['speaker'] != speaker)
#             ]
            
#             # Sum talk_move_count for these other speakers and get their IDs
#             received_talkmove = other_speakers_in_session['talk_move_count'].sum()
#             received_ids = other_speakers_in_session['speaker'].unique().tolist()

#             # Append results for this session to the lists
#             received_talkmove_counts.append(received_talkmove)
#             received_speaker_ids.append(received_ids)

#         # Flatten the list of received talk move counts and speaker IDs for this speaker
#         total_received_talkmove = sum(received_talkmove_counts)  # Sum of all received talk moves
#         flattened_received_ids = [item for sublist in received_speaker_ids for item in sublist]

#         # Append to the summary data
#         summary_data['speaker'].append(speaker)
#         summary_data['session_IDs'].append(session_IDs)
#         summary_data['talk_move_counts'].append(talk_move_counts)
#         summary_data['total_talk_move_count'].append(total_talk_move_count)
#         summary_data['merge_note'].append(merge_note)
#         summary_data['received_student_talkmove'].append(received_talkmove_counts)
#         summary_data['student_id_received_talkmove'].append(flattened_received_ids)
#         summary_data['sum_received_student_talkmove'].append(total_received_talkmove)

#     # Create a DataFrame from the summary data
#     summary_df = pd.DataFrame(summary_data)

#     # Save the summary DataFrame to a new CSV file
#     summary_df.to_csv(output_file, index=False)
#     print(f"Summary file saved as '{output_file}'.")

#     return summary_df

# # Example usage
# summary_df = summarize_talk_moves_with_received_talkmove(
#     file_path=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\speaker-utterances-2023-08-01-to-2024-06-14.csv',
#     output_file=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\summary_talk_moves_with_received3.csv'
# )


# #Merge and Summarize Talkmove by Summing
# def summarize_talk_moves_with_received_talkmove(file_path: str, output_file: str):
#     """
#     Summarizes talk moves for each unique 'speaker_id' where 'speaker_type' is 'student'.
#     Produces a CSV file containing each unique 'speaker_id', a list of 'session_ID's,
#     a list of 'talk_move_count's per session, a column for total 'talk_move_count' sum,
#     a 'merge_note' column for cases where session IDs were summed,
#     columns for received student and tutor talk moves, IDs, and total sums.
    
#     Args:
#     - file_path (str): The path to the input CSV file (e.g., 'preprocessed_final.csv').
#     - output_file (str): The path to save the summarized output CSV file.
    
#     Returns:
#     - summary_df (pd.DataFrame): The resulting DataFrame with summarized talk moves and merge notes.
#     """
#     # Load the CSV file
#     df = pd.read_csv(file_path)

#     # Filter for rows where 'speaker_type' is 'student' and language is 'en'
#     english_df = df[df['language'] == 'en']
#     student_df = english_df[english_df['speaker_type'] == 'student']

#     # Group by 'speaker_id' and aggregate data
#     summary_data = {
#         'speaker': [],
#         'session_IDs': [],
#         'talk_move_counts': [],
#         'total_talk_move_count': [],
#         'merge_note': [],
#         'received_student_talkmove': [],
#         'student_id_received_talkmove': [],
#         'sum_received_student_talkmove': [],
#         'received_tutor_talkmove': [],
#         'tutor_id_received_talkmove': [],
#         'sum_received_tutor_talkmove': []
#     }

#     for speaker, group in student_df.groupby('speaker'):
#         # Count occurrences of each session_ID
#         session_counts = group['session_ID'].value_counts()
#         duplicate_sessions = session_counts[session_counts > 1].index.tolist()
        
#         # Get unique session IDs and corresponding talk move counts
#         session_IDs = group['session_ID'].unique().tolist()
#         talk_move_counts = group.groupby('session_ID')['talk_move_count'].sum().tolist()
        
#         # Sum all talk move counts for the current speaker
#         total_talk_move_count = sum(talk_move_counts)
        
#         # Set merge note if there were any duplicate sessions
#         merge_note = "speech and chat summed" if duplicate_sessions else ""

#         # Initialize lists to store received talk move counts and IDs
#         received_student_talkmove_counts = []
#         received_student_ids = []
#         received_tutor_talkmove_counts = []
#         received_tutor_ids = []

#         # Iterate through each unique session for this speaker
#         for session in session_IDs:
#             # Student talk moves (other students in the same session)
#             other_students_in_session = student_df[
#                 (student_df['session_ID'] == session) &
#                 (student_df['speaker'] != speaker)
#             ]
#             received_student_talkmove = other_students_in_session['talk_move_count'].sum()
#             student_ids = other_students_in_session['speaker'].unique().tolist()
#             received_student_talkmove_counts.append(received_student_talkmove)
#             received_student_ids.append(student_ids)

#             # Tutor talk moves (tutors in the same session)
#             tutors_in_session = english_df[
#                 (english_df['session_ID'] == session) &
#                 (english_df['speaker_type'] == 'tutor')
#             ]
#             received_tutor_talkmove = tutors_in_session['talk_move_count'].sum()
#             tutor_ids = tutors_in_session['speaker'].unique().tolist()
#             received_tutor_talkmove_counts.append(received_tutor_talkmove)
#             received_tutor_ids.append(tutor_ids)

#         # Flatten the list of received student and tutor IDs, and compute total received talk moves
#         total_received_student_talkmove = sum(received_student_talkmove_counts)
#         flattened_received_student_ids = [item for sublist in received_student_ids for item in sublist]

#         total_received_tutor_talkmove = sum(received_tutor_talkmove_counts)
#         flattened_received_tutor_ids = [item for sublist in received_tutor_ids for item in sublist]

#         # Append to the summary data
#         summary_data['speaker'].append(speaker)
#         summary_data['session_IDs'].append(session_IDs)
#         summary_data['talk_move_counts'].append(talk_move_counts)
#         summary_data['total_talk_move_count'].append(total_talk_move_count)
#         summary_data['merge_note'].append(merge_note)
#         summary_data['received_student_talkmove'].append(received_student_talkmove_counts)
#         summary_data['student_id_received_talkmove'].append(received_student_ids)  # List of lists
#         summary_data['sum_received_student_talkmove'].append(total_received_student_talkmove)
#         summary_data['received_tutor_talkmove'].append(received_tutor_talkmove_counts)
#         summary_data['tutor_id_received_talkmove'].append(received_tutor_ids)  # List of lists
#         summary_data['sum_received_tutor_talkmove'].append(total_received_tutor_talkmove)

#     # Create a DataFrame from the summary data
#     summary_df = pd.DataFrame(summary_data)

#     # Save the summary DataFrame to a new CSV file
#     summary_df.to_csv(output_file, index=False)
#     print(f"Summary file saved as '{output_file}'.")

#     return summary_df

# # Example usage
# summary_df = summarize_talk_moves_with_received_talkmove(
#     file_path=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\speaker-utterances-2023-08-01-to-2024-06-14.csv',
#     output_file=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\summary_talk_moves_with_received_tutor.csv'
# )


def summarize_talk_moves_with_received_talkmove(file_path: str, output_file: str):
    """
    Summarizes talk moves for each unique 'speaker_id' where 'speaker_type' is 'student' using averages.
    Produces a CSV file containing each unique 'speaker_id', a list of 'session_ID's,
    a list of 'talk_move_count' averages per session, a column for overall average talk move,
    a 'merge_note' column for cases where session IDs were summed,
    columns for received student and tutor talk moves, IDs, and overall averages.
    
    Args:
    - file_path (str): The path to the input CSV file (e.g., 'preprocessed_final.csv').
    - output_file (str): The path to save the summarized output CSV file.
    
    Returns:
    - summary_df (pd.DataFrame): The resulting DataFrame with summarized talk moves and merge notes.
    """
    
    
    
    # Load the CSV file
    df = pd.read_csv(file_path)
    

    # Filter for rows where 'speaker_type' is 'student' and language is 'en'
    english_df = df[df['language'] == 'en']
    student_df = english_df[english_df['speaker_type'] == 'student']

    # Group by 'speaker_id' and aggregate data
    summary_data = {
        'speaker': [],
        'session_IDs': [],
        'talkmove_ratio': [],
        'average_talk_move_count': [],
        'merge_note': [],
        'received_student_talkmove': [],
        'student_id_received_talkmove': [],
        'average_received_student_talkmove': [],
        'received_tutor_talkmove': [],
        'tutor_id_received_talkmove': [],
        'average_received_tutor_talkmove': []
    }

    for speaker, group in student_df.groupby('speaker'):
        # Count occurrences of each session_ID
        session_counts = group['session_ID'].value_counts()
        duplicate_sessions = session_counts[session_counts > 1].index.tolist()
        
        # Get unique session IDs and corresponding talk move counts (averages this time)
        session_IDs = group['session_ID'].unique().tolist()
        talkmove_ratio = group.groupby('session_ID')['talk_move_count'].mean().tolist()
        
        # Calculate the overall average talk move count for the current speaker
        average_talk_move_count = sum(talkmove_ratio) / len(talkmove_ratio) if talkmove_ratio else 0
        
        # Set merge note if there were any duplicate sessions
        merge_note = "speech and chat summed" if duplicate_sessions else ""

        # Initialize lists to store received talk move counts and IDs
        received_student_talkmove_ratio = []
        received_student_ids = []
        received_tutor_talkmove_ratio = []
        received_tutor_ids = []

        # Iterate through each unique session for this speaker
        for session in session_IDs:
            # Student talk moves (other students in the same session)
            other_students_in_session = student_df[
                (student_df['session_ID'] == session) &
                (student_df['speaker'] != speaker)
            ]
            received_student_talkmove = other_students_in_session['talk_move_count'].mean()
            student_ids = other_students_in_session['speaker'].unique().tolist()
            received_student_talkmove_ratio.append(received_student_talkmove)
            received_student_ids.append(student_ids)

            # Tutor talk moves (tutors in the same session)
            tutors_in_session = english_df[
                (english_df['session_ID'] == session) &
                (english_df['speaker_type'] == 'tutor')
            ]
            received_tutor_talkmove = tutors_in_session['talk_move_count'].mean()
            tutor_ids = tutors_in_session['speaker'].unique().tolist()
            received_tutor_talkmove_ratio.append(received_tutor_talkmove)
            received_tutor_ids.append(tutor_ids)

        # Calculate overall averages for received talk moves
        average_received_student_talkmove = sum(received_student_talkmove_ratio) / len(received_student_talkmove_ratio) if received_student_talkmove_ratio else 0
        average_received_tutor_talkmove = sum(received_tutor_talkmove_ratio) / len(received_tutor_talkmove_ratio) if received_tutor_talkmove_ratio else 0

        # Append to the summary data
        summary_data['speaker'].append(speaker)
        summary_data['session_IDs'].append(session_IDs)
        summary_data['talkmove_ratio'].append(talkmove_ratio)
        summary_data['average_talk_move_count'].append(average_talk_move_count)
        summary_data['merge_note'].append(merge_note)
        summary_data['received_student_talkmove'].append(received_student_talkmove_ratio)
        summary_data['student_id_received_talkmove'].append(received_student_ids)  # List of lists
        summary_data['average_received_student_talkmove'].append(average_received_student_talkmove)
        summary_data['received_tutor_talkmove'].append(received_tutor_talkmove_ratio)
        summary_data['tutor_id_received_talkmove'].append(received_tutor_ids)  # List of lists
        summary_data['average_received_tutor_talkmove'].append(average_received_tutor_talkmove)

    # Create a DataFrame from the summary data
    summary_df = pd.DataFrame(summary_data)

    # Save the summary DataFrame to a new CSV file
    summary_df.to_csv(output_file, index=False)
    print(f"Summary file saved as '{output_file}'.")

    return summary_df

# Example usage
summary_df = summarize_talk_moves_with_received_talkmove(
    file_path=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\speaker-utterances-2023-08-01-to-2024-06-14_merged_mode.csv',
    output_file=r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\summary_talk_moves_with_received_avg.csv'
)

