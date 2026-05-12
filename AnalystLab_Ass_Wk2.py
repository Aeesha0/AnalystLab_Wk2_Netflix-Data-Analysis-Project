import pandas as pd 

# ==========================================
# PHASE 1 & 2: IMPORT, STRUCTURE & AUDIT
# ==========================================

# 1. Load the dataset
df = pd.read_csv('C:\\Users\\DELL\\python.py\\MydataAnalysisProject\\AnalystLab_Project\\Aishat_Wk2_Project\\netflix_titles.csv')

print("--- INITIAL DATA AUDIT ---")
print(f"Dataset Shape: {df.shape}")
print("\nColumn Info:")
df.info()

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

# ==========================================
# PHASE 3: DATA CLEANING
# ==========================================

# 1. Categorical Imputation (Logical Filling)
# We fill these to preserve row volume for general analysis
df['director'] = df['director'].fillna('Unknown Director')
df['cast'] = df['cast'].fillna('No Cast Listed')
df['country'] = df['country'].fillna('Unknown Country')

# 2. Date Standardization
df['date_added'] = pd.to_datetime(df['date_added'].str.strip())

# Since there are only 10 missing dates (0.1%), we drop them to ensure timeline accuracy
df.dropna(subset=['date_added'], inplace=True)

# We Extract the Year for Trend Analysis
df['year_added'] = df['date_added'].dt.year.astype(int)

# 3. Statistical Imputation (Mode Filling)
# Handling the remaining 4 nulls in Rating and 3 in Duration
df['rating'] = df['rating'].fillna(df['rating'].mode()[0])
df['duration'] = df['duration'].fillna(df['duration'].mode()[0])

# 4. Text Standardization: Ensuring categories like 'Movie' and 'movie' are treated as the same
df['type'] = df['type'].str.strip().str.title()
df['rating'] = df['rating'].str.strip().str.upper()


print("\n--- FINAL INTEGRITY CHECK ---")
print(df.isnull().sum())
print(f"\nFinal Cleaned Row Count: {len(df)}")

# the cleaned dataset for reference
df.to_csv('Netflix_Cleaned_Aishat.csv', index=False)
print("\nSUCCESS: Cleaned data saved to 'Netflix_Cleaned_Aishat.csv'")

#  Exploratory Data Analysis and Visualizations
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# ==========================================
# 1. VISUAL: Content Type Distribution (Pie Chart)
# ==========================================
plt.figure(figsize=(8, 8))
type_counts = df['type'].value_counts()
plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', 
        colors=['#E50914', '#221F1F'], startangle=140, explode=(0.05, 0))
plt.title('Netflix Content Strategy: Movies vs TV Shows', fontsize=14, fontweight='bold')
plt.savefig('netflix_type_distribution.png')
print("Saved Visual 1: netflix_type_distribution.png")

# ==========================================
# 2. VISUAL: Growth Trend (Line Chart)
# ==========================================
plt.figure(figsize=(12, 6))
# We do the grouping by year_added and count the show_id
growth_data = df.groupby('year_added').size()
sns.lineplot(x=growth_data.index, y=growth_data.values, marker='o', color='#E50914', linewidth=2.5)
plt.title('Content Expansion Over Time (2008 - 2021)', fontsize=14, fontweight='bold')
plt.xlabel('Year Content was Added')
plt.ylabel('Total Titles Added')
plt.savefig('netflix_growth_trend.png')
print("Saved Visual 2: netflix_growth_trend.png")

# ==========================================
# 3. VISUAL: Top 10 Countries using Bar Chart
# ==========================================
# REPLACE JUST THIS SECTION TO REMOVE THE ERROR
plt.figure(figsize=(12, 6))
df['primary_country'] = df['country'].str.split(',').str[0]
top_10_countries = df['primary_country'].value_counts().head(10)

# The fix: Adding hue and setting legend to False
sns.barplot(
    x=top_10_countries.values, 
    y=top_10_countries.index, 
    hue=top_10_countries.index, 
    palette='Reds_r', 
    legend=False
)
plt.title('Top 10 Content Producing Countries', fontsize=14, fontweight='bold')
plt.xlabel('Count of Titles')
plt.ylabel('Country')
plt.savefig('netflix_top_countries.png')
print("Saved Visual 3: netflix_top_countries.png")



# Display all plots
plt.show()

import os

# 1. Define the exact folder path
folder_path = r'C:\\Users\\DELL\\python.py\\MydataAnalysisProject\\AnalystLab_Project\\Aishat_Wk2_Project'

# 2. Define the full file name
full_file_path = os.path.join(folder_path, 'Netflix_Cleaned_Aishat.csv')

# 3. Save the dataframe to that specific location
df.to_csv(full_file_path, index=False)

print(f"Process Complete! Check your folder now: {full_file_path}")