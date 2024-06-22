# Link to the challenge
# https://www.linkedin.com/posts/dinc-doga-660113307_new-challange-for-table-transformation-with-activity-7210286997318336512-OtqB/

import pandas as pd

# Read the Excel file
file_path = 'Chl_002.xlsx'
df = pd.read_excel(file_path, nrows=6, usecols='B:L', skiprows=1)

# Perform data wrangling
columns = [float('nan') if col.startswith('Un') else col for col in df.columns]
columns = pd.DataFrame(columns, columns=['Names']).ffill()
df.columns = columns['Names']
row = df.iloc[0].replace(float('nan'), '')
df.columns = [f"{'_'.join([col, row[i]]) if row[i] else col}" for i, col in enumerate(df.columns)]
df = df.drop(0, axis=0)
df = df.melt(id_vars=['Elevation', 'Region'], value_vars=df.columns[2: ])

df = pd.concat([df, df['variable'].str.split('_', expand=True)], axis=1)
df = df.drop(columns='variable').iloc[:, [0, 1, 3, 4, 2]]
df = df.rename(columns={0: 'Work'})
df = df.pivot(index=['Elevation', 'Region', 'Work'], columns=1, values='value').reset_index()
df = df.iloc[:, [0, 1, 2, 5, 3, 4]][df['Duration'] != 0]
df = df.sort_values(by=['Duration', 'Region'], ignore_index=True)

# Display the final dataset
df
