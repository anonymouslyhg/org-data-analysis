# 1. Import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from google.colab import files
from collections import Counter

# 2. Load and preprocess 'organizations.csv' file

data = pd.read_csv("organizations.csv") # download from here (https://drive.usercontent.google.com/download?id=18vlOi20KcMR328ewc2NBsoBNPrV3vL9Q&export=download&authuser=0)
# 3. Aggregate top countries, industries, and websites per organization
org_office_number = data['Name'].value_counts()
org_office_df = org_office_number.reset_index()
grouped_counts = data.groupby('Name', sort=False)['Country'].value_counts()
top_countries_per_name = grouped_counts.groupby(level=0, sort=False).head(4)

industry_group_counts = data.groupby('Name', sort=False)['Industry'].value_counts()
top_industries_per_name = industry_group_counts.groupby(level=0, sort=False).head(4)



com_industry_name = []
for name, group_data in top_industries_per_name.groupby(level=0):
  com_industry_name.append({
      'Name': name,
      'Industry': group_data.index.get_level_values(1).tolist()
  })
top_industry_df = pd.DataFrame(com_industry_name)

com_country_name_optimized = []
for name, group_data in top_countries_per_name.groupby(level=0):
    com_country_name_optimized.append({
        'Name': name,
        'Country': group_data.index.get_level_values(1).tolist()
    })
top_country_df_optimized = pd.DataFrame(com_country_name_optimized)
# 4. Merge various groupings into a single DataFrame (`new_df`)
merged_data = pd.merge(
    org_office_df,
    top_country_df_optimized,
    how='left',
    on='Name'
)
employee_sum = data.groupby('Name', as_index=False)['Number of employees'].sum()
employees_average = data.groupby('Name', as_index=False)['Number of employees'].mean()
new_data = pd.merge(
    merged_data,
    employee_sum,
    how='left',
    on='Name'
)
new_data_avg_employ = pd.merge(
    new_data,
    employees_average,
    how='left',
    on='Name'
)
new_data_industry = pd.merge(
    new_data_avg_employ,
    top_industry_df,
    how='left',
    on='Name'
)
website_group_counts = data.groupby('Name', sort=False)['Website'].value_counts()
top_websites_per_name = website_group_counts.groupby(level=0, sort=False).head(4)

com_website_name = []
for names, group_data in top_websites_per_name.groupby(level=0):
  com_website_name.append({
      'Name': names,
      'Website': group_data.index.get_level_values(1).tolist()
  })
top_website_df_optimized = pd.DataFrame(com_website_name)

new_data_website = pd.merge(
    new_data_industry,
    top_website_df_optimized,
    how='left',
    on='Name'
)
#year_found = data.groupby(new_data['Name'], as_index=False)['Founded'].first()
#print(year_found)
filter = data[data['Name'].isin(new_data['Name'])]
year_found = filter.groupby('Name', as_index=False)['Founded'].min()
new_df = pd.DataFrame({
    'Organization_Name' : new_data['Name'],
    'Number_of_Offices' : new_data['count'],
    'Country' : new_data['Country'],
    'Number_Of_Employees' : new_data['Number of employees'],
    'Average_No_Of_Employ' : new_data_avg_employ['Number of employees_y'].astype(int),
    'Year_Founded' : year_found['Founded'],
    'Industry' : new_data_industry['Industry'],
    'Website' : new_data_website['Website']
})
# 5. Export processed data as CSV
new_df.to_csv("Updated Data.csv", index=False)
#files.download("Updated Data.csv") # This will only work for google colab

# 6. Analytics Part Begins 
# Setup
custom_palette = [
    '#005073', '#107dac'
]
sns.set_style('whitegrid')
custom_palette = sns.color_palette('muted')
sns.set_palette(custom_palette)

# Top 20 orgs by employees
top_orgs = new_df.sort_values(by='Number_Of_Employees', ascending=False).head(20)

# 1. Bar: Employees per org
plt.figure(figsize=(14, 6))
sns.barplot(data=top_orgs, x='Organization_Name', y='Number_Of_Employees')
plt.title('Top 20 Organizations by Number of Employees')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 2. Bar: Offices per org
plt.figure(figsize=(14, 6))
sns.barplot(data=top_orgs, x='Organization_Name', y='Number_of_Offices')
plt.title('Top 20 Organizations by Number of Offices')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 3. Scatter: Offices vs Employees
plt.figure(figsize=(8, 6))
sns.scatterplot(data=new_df, x='Number_of_Offices', y='Number_Of_Employees')
plt.title('Employees vs Offices')
plt.tight_layout()
plt.show()

# 4. Bar: Average Employees per Office
plt.figure(figsize=(14, 6))
sns.barplot(data=top_orgs, x='Organization_Name', y='Average_No_Of_Employ')
plt.title('Average Employees per Office')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 5. Histogram: Employee distribution
plt.figure(figsize=(10, 6))
sns.histplot(data=new_df, x='Number_Of_Employees', bins=40, kde=True)
plt.title('Distribution of Employee Counts')
plt.tight_layout()
plt.show()

# 6. Count: Organizations by Year Founded
plt.figure(figsize=(12, 6))
sns.countplot(data=new_df, x='Year_Founded')
plt.title('Organizations Founded by Year')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 7. Bar: Top 10 Countries
all_countries = sum(new_df['Country'].dropna().tolist(), [])
country_counts = Counter(all_countries)
top_countries = dict(country_counts.most_common(10))
country_df = pd.DataFrame(top_countries.items(), columns=['Country', 'Count'])

plt.figure(figsize=(10, 6))
sns.barplot(data=country_df, y='Country', x='Count')
plt.title('Top 10 Most Frequent Countries')
plt.tight_layout()
plt.show()

# 8. Bar: Top 10 Industries
all_industries = sum(new_df['Industry'].dropna().tolist(), [])
industry_counts = Counter(all_industries)
top_industries = dict(industry_counts.most_common(10))
industry_df = pd.DataFrame(top_industries.items(), columns=['Industry', 'Count'])

plt.figure(figsize=(10, 6))
sns.barplot(data=industry_df, y='Industry', x='Count')
plt.title('Top 10 Most Frequent Industries')
plt.tight_layout()
plt.show()

# 9. Pie Chart: Top 5 Countries
top5_countries = dict(country_counts.most_common(5))
plt.figure(figsize=(6, 6))
plt.pie(top5_countries.values(), labels=top5_countries.keys(), autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Top 5 Country Distribution')
plt.axis('equal')
plt.tight_layout()
plt.show()

# 10. Line: Year Founded vs Avg Employee Count
year_emp = new_df.groupby('Year_Founded')['Number_Of_Employees'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=year_emp, x='Year_Founded', y='Number_Of_Employees')
plt.title('Average Employees by Year Founded')
plt.tight_layout()
plt.show()

# 11. Pair Plot: Compare numeric columns
sns.pairplot(new_df[['Number_of_Offices', 'Number_Of_Employees', 'Average_No_Of_Employ']])
plt.suptitle("Pairwise Relationship Between Key Metrics", y=1.02)
plt.show()
