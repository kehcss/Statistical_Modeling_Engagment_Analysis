import pandas as pd

def process_student_data(file_path):
    """
    Reads the student data CSV, calculates the 'Final_score' for each row,
    and calculates the number of unique session_IDs, unique student_id_received_talkmove,
    and unique tutor_id_received_talkmove values for each row.
    """
    # Read the CSV file
    student_data = pd.read_csv(file_path)
    
    # # Calculate Final_score using the formula 'Initial_score' + ('Slope' * 3)
    # student_data['Final_score'] = student_data['Intercept'] + (student_data['Slope'] * 3)
    
    # Rename 'speaker' to 'student_ID'
    student_data.rename(columns={'speaker': 'student_ID'}, inplace=True)
    
    # Convert 'student_ID' and 'tutor_ID' to string type for consistent merging
    student_data['student_ID'] = student_data['student_ID'].astype(str)
    student_data['tutor_ID'] = student_data['tutor_ID'].astype(str)
    
    # Calculate unique counts for session_IDs, student_id_received_talkmove, and tutor_id_received_talkmove
    student_data['unique_session_IDs_count'] = student_data['session_IDs'].apply(lambda x: len(set(eval(x))))
    student_data['unique_student_id_received_talkmove_count'] = student_data['student_id_received_talkmove'].apply(lambda x: len(set(sum(eval(x), []))))
    student_data['unique_tutor_id_received_talkmove_count'] = student_data['tutor_id_received_talkmove'].apply(lambda x: len(set(sum(eval(x), []))))
    
    return student_data


def merge_survey_data(student_data, survey_file_path):
    """
    Merges survey data into the previously processed student data on 'Anonymized_student_ID'
    and returns the final merged DataFrame.
    """
    # Read the survey data CSV file
    survey_data = pd.read_csv(survey_file_path)
    
    # Rename the column
    survey_data.rename(columns={'Anon Student ID': 'Anonymized student ID'}, inplace=True)
        
    # Convert 'Anonymized student ID' to string type in both datasets
    student_data['Anonymized student ID'] = student_data['Anonymized student ID'].astype(str)
    survey_data['Anonymized student ID'] = survey_data['Anonymized student ID'].astype(str)
    
    # Debugging print statements to check columns
    print("Student Data Columns:", student_data.columns)
    print("Survey Data Columns:", survey_data.columns)
    
    # Merge on 'Anonymized student ID'
    final_merged = pd.merge(student_data, survey_data, on='Anonymized student ID', how='left')
    
    return final_merged

def main():
    # Define file paths
    student_file = r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\january3rd_summary_talk_moves.csv'
    survey_file = r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\code\FactorScores.csv'
    output_file = r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\code\processed_summary_of_speaker-utterances_jan04.csv'
    
    # Process student data and calculate Final_score
    student_data = process_student_data(student_file)

    # Merge with survey data to get the final dataset
    final_data = merge_survey_data(student_data, survey_file)
    
    # Save the final data to a new CSV file
    final_data.to_csv(output_file, index=False)
    print(f"Data has been successfully processed and saved to '{output_file}'.")

if __name__ == '__main__':
    main()
