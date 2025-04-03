import pandas as pd

# Load the CSV file
df = pd.read_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\Student_Achievement_Intercept_Slope_10_23_2024.csv')

# Drop rows where 'student_ID' is NaN
df = df.dropna(subset=['student_ID'])


# Convert all student IDs and other relevant columns to string for consistent processing
df['student_ID'] = df['student_ID'].astype(str)
df['coach_ID'] = df['coach_ID'].astype(str)
df['tutor_ID'] = df['tutor_ID'].astype(str)
df['Intercept'] = df['Intercept'].astype(str)

# Find duplicate student IDs
duplicates = df['student_ID'].value_counts()
duplicates = duplicates[duplicates > 1]

# Filter the DataFrame to only include rows with duplicate student IDs
df_duplicates = df[df['student_ID'].isin(duplicates.index)]

# Group by 'student_ID' and aggregate the unique values in other columns
grouped_duplicates = df_duplicates.groupby('student_ID').agg({
    'student_ID': 'size',  # Directly count occurrences of each student_ID
    'coach_ID': lambda x: set(x),
    'tutor_ID': lambda x: set(x),
    'Intercept': lambda x: set(x)
}).rename(columns={'student_ID': 'Count'}).reset_index()  # Rename the counted column to 'Count'
# Add an index column
grouped_duplicates['Index'] = grouped_duplicates.index + 1

# Reorder columns to have 'Index' as the first column
grouped_duplicates = grouped_duplicates[['Index', 'student_ID', 'Count', 'coach_ID', 'tutor_ID', 'Intercept']]

# Print the results
print("Duplicate Student IDs and their associated values with counts:")
print(grouped_duplicates)


# Save to CSV
grouped_duplicates.to_csv(r'C:\Users\keez8796\Emotive Computing Dropbox\Kelechi Ezema\student_engagement\data\dubplicate_Student_Achievement.csv', index=False)