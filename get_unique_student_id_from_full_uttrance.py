import pandas as pd

# Load the Student CSV file into a DataFrame
df = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\speaker-utterances_talkmove_ratio_merged_mode.csv')

# # Get the unique student
# unique_student_ids = df['student_ID'].unique()

# # Create a DataFrame with the unique student
# unique_student_ids_df = pd.DataFrame(unique_student_ids, columns=['student_ID'])

# # Load Tutor CSV file into a DataFrame
# df = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\final_procssed_student_level.csv')


#check the number of student_IDs in each row
df['student_IDs'] = df['student_IDs'].fillna('')
df['student_IDs'] = df['student_IDs'].str.split(';')
df['student_IDs_in_session_count'] = df['student_IDs'].apply(lambda x: len(x))

