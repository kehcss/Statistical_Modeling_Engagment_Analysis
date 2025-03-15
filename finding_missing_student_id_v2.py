import pandas as pd
import numpy as np


# Load the data
missing_data = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\student_with_missing_achievement_details.csv')
fsa_data = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\curated-FSA - curated-FSA-updated.csv')
star_data = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\curated-STAR - curated-STAR-updated.csv')
site_director = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\Tutor, SD and Site IDs - Site Director List.csv')
user_with_missing_region= pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\Tutor, SD and Site IDs - Users with missing region.csv')
full_tutor_data = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\Saga Tutor Attrition Data 23-24 - Saga Tutor Attrition Data 23-24.csv')
saga_ann_id = pd.read_excel(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\2024 Saga Crosswalk - Student IDs.xlsx')
student_achievemt = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\Student_Achievement_Intercept_Slope_10_23_2024.csv')
sandra_file = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\Jan 2025 - CU_FSA&STAR Review - Student info + CU_Star.csv')

# Convert all student ID columns to string to ensure consistency
missing_data['student_ID'] = missing_data['student_ID'].astype(str)
fsa_data['student_ID'] = fsa_data['student_ID'].astype(str)
star_data['student_ID'] = star_data['student_ID'].astype(str)
site_director['site director ID'] = site_director['site director ID'].astype(str)
user_with_missing_region['ID'] = user_with_missing_region['ID'].astype(str)
full_tutor_data['Ajusted ID'] = full_tutor_data['Ajusted ID'].astype(str)
saga_ann_id['Saga Student ID'] = saga_ann_id['Saga Student ID'].astype(str)
student_achievemt['tutor_ID'] = student_achievemt['tutor_ID'].astype(str)
sandra_file['user_id'] = sandra_file['user_id'].astype(str)

# Check for existence of student_IDs in different dataframes
missing_data['is_in_FSA'] = missing_data['student_ID'].isin(fsa_data['student_ID']).astype(int)
missing_data['is_in_STAR'] = missing_data['student_ID'].isin(star_data['student_ID']).astype(int)
missing_data['is_in_Site_directors'] = missing_data['student_ID'].isin(site_director['site director ID']).astype(int)
missing_data['is_in_user_missing_region'] = missing_data['student_ID'].isin(user_with_missing_region['ID']).astype(int)
missing_data['is_in_full_tutor'] = missing_data['student_ID'].isin(full_tutor_data['Ajusted ID']).astype(int)
missing_data['is_in_achievement_tutor'] = missing_data['student_ID'].isin(student_achievemt['tutor_ID']).astype(int)
missing_data['has_anonymous_student_id'] = missing_data['student_ID'].isin(saga_ann_id['Saga Student ID']).astype(int)

# First, create a filtered list of user_id that are marked as different type
old_tutors = sandra_file[sandra_file['Type'] == 'Old Tutor']['user_id'].astype(str)
fake_student = sandra_file[sandra_file['Type'] == 'Fake students']['user_id'].astype(str)
cross_walk_issues = sandra_file[sandra_file['Found in the Last Round Crosswalk 0 = not in list 1 = in list'] != 0]['user_id'].astype(str)

# Now check if each student_ID in missing_data is in this list
missing_data['is_old_tutor'] = missing_data['student_ID'].isin(old_tutors).astype(int)
missing_data['is_fake_student'] = missing_data['student_ID'].isin(fake_student).astype(int)
missing_data['need_crosswalk_fixing'] = missing_data['student_ID'].isin(cross_walk_issues).astype(int)


#Speaker type categorization
# Define the conditions for categorizing 'speaker_type'
conditions = [
    (missing_data['is_old_tutor'] == 1) | (missing_data['is_in_full_tutor'] == 1) | (missing_data['is_in_achievement_tutor'] == 1) | (missing_data['is_fake_student'] == 1),
    (missing_data['is_in_Site_directors'] == 1) | (missing_data['is_in_user_missing_region'] == 1),
    
]

# Define the corresponding values for 'speaker_type'
choices = ['tutor_student', 'admin_user']

# Use numpy.select to apply these conditions and choices
missing_data['speaker_type'] = np.select(conditions, choices, default='student')




# Save to CSV
missing_data.to_excel(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\student_id_not_found_in_achievement_updated_jan28.xlsx', index=False)