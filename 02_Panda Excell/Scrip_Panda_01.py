import numpy as np
import pandas as pd


data = [50,50,47,97,49,3,53,42,26,74,82,62,37,15,70,27,36,35,48,52,63,64]
grades = np.array(data)
grades.shape

# Define an array of study hours
study_hours = [10.0,11.5,9.0,16.0,9.25,1.0,11.5,9.0,8.5,14.5,15.5,13.75,9.0,8.0,15.5,8.0,9.0,6.0,10.0,12.0,12.5,12.0]

# Create a 2D array (an array of arrays)
student_data = np.array([study_hours, grades])
# Create a 2D array (an array of arrays)
student_data = np.array([study_hours, grades])
# display the array
student_data

df_students = pd.DataFrame({'Name': ['Dan', 'Joann', 'Pedro', 'Rosie', 'Ethan', 'Vicky', 'Frederic', 'Jimmie', 
                                     'Rhonda', 'Giovanni', 'Francesca', 'Rajab', 'Naiyana', 'Kian', 'Jenny',
                                     'Jakeem','Helena','Ismat','Anila','Skye','Daniel','Aisha'],
                            'StudyHours':student_data[0],
                            'Grade':student_data[1]})

print(df_students) 
print()

# Get the data for index value 5
print("Get the data for index value 5")
print(df_students.loc[5])
print()

# Get the rows with index values from 0 to 5
print("Get the rows with index values from 0 to 5")
print(df_students.loc[0:5])
print()

# Get data in the first five rows
print("Get data in the first five rows")
print(df_students.iloc[0:5])
print()

# Get firs row and column 1 and 2
print("Get firs row and column 1 and 2")
print(df_students.iloc[0,[1,2]])
print()

# Gets studen with name Aisha
print("Gets studen with name Aisha")
print(df_students.loc[df_students['Name']=='Aisha'])
print()

# Gets studen with name Aisha based on Query (easier)
print("Gets studen with name Aisha based on Query (easier)")
print(df_students.query('Name=="Aisha"'))
print()

# Gets studen with StudyHours == 10
print("Gets studen with StudyHours = 10")
print(df_students.loc[df_students['StudyHours']==12])
print()

# Gets studen with StudyHours >10
print("Gets studen with StudyHours > 10")
print(df_students.loc[df_students['StudyHours']>10])
print()