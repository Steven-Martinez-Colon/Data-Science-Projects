#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:45:40 2023

@author: stevenmartinez
"""

#%% libraries

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

#%% importing the data

cost_of_living_df = pd.read_csv('/Users/stevenmartinez/Documents/Merrimack Classes/ R and Python DSE5002/Python Project/Data/cost_of_living.csv')
ds_salaries_df = pd.read_csv('/Users/stevenmartinez/Documents/Merrimack Classes/ R and Python DSE5002/Python Project/Data/ds_salaries.csv')
levels_salary_df = pd.read_csv('/Users/stevenmartinez/Documents/Merrimack Classes/ R and Python DSE5002/Python Project/Data/Levels_Fyi_Salary_Data.csv')
country_codes_df = pd.read_excel('/Users/stevenmartinez/Documents/Merrimack Classes/ R and Python DSE5002/Python Project/Data/country_codes.xlsx')


#%% Finding the top 5 cities for a hispanic person that works as a data scientist

# Creating a data frame focusing on Hispanic race, Master's Degree, and Data Scientist
hispanic_df = levels_salary_df[(levels_salary_df['Race_Hispanic'] == 1) &
                               (levels_salary_df['Masters_Degree'] == 1) &
                               (levels_salary_df['title'] == 'Data Scientist')]

# Showing that hispanic_df has a low number of observations
print(hispanic_df.shape)

# Creating a data frame focusing on Hispanic race and Data Scientist
hispanic_df_no_masters = levels_salary_df[(levels_salary_df['Race_Hispanic'] == 1) &
                               (levels_salary_df['title'] == 'Data Scientist')]

# Showing that hispanic_df_no_masters has a low number of observations
hispanic_df_no_masters.shape

# Finding the indices of the top 5 salaries
print(hispanic_df['basesalary'].nlargest(n=5))

# Creating a data frame with the names of the top 5 cities and the corresponding salaries for hispanic race
hispanic_top_five_cities = levels_salary_df.iloc[[55713, 48043, 39969, 29042, 53838], [5, 9]]

#%% Data scientist diversity issue

# Creating a data frame with just data scientists
data_scientist_df = levels_salary_df[(levels_salary_df['title'] == 'Data Scientist')]

# Finding out how many data scientest there are by race
print(data_scientist_df.groupby(['Race']).size())
z = pd.DataFrame({'Race':['Asian', 'Black', 'Hispanic', 'Two Or More', 'White'],
                  'Count': [505, 13, 32, 28, 317]})

# Set up the figure and theme
sns.set_theme(style="darkgrid")
plt.figure(figsize = (10, 6))

# Drawing a barplot to show the number of data scietist by race
sns.barplot(
    data = z,
    x="Race",
    y = 'Count'
)
plt.title("Number of Data Scientist by Race")


# Subsetting by Hispanic race did not give me enough data to make a decision. There were only
# 12 hispanics that are data scientist and have a master's degree. I then did another subset
# but removed the master's degree and got only 32 rows. Once again, I was not satisfied
# with the amount of data. I then looked at the number of data scientists by race and 
# what the barplot shows is interesting. It seems like there isn't much diversity in the
# data science field. This got me wondering why there aren't more hispanics or blacks
# working ont his field? This is a question to answer another day. However, as a Hispanic
# myself, this is something that I am passionate about and would love to change.
# Now that I am done going on this tangent, lets get back to finding out the top 5 cities.

#%% Plotting the data scientists base salaries

# Data frame with just data scientists
data_scientist_df

# Drawing a histogram to see the shape of the base salary for data scientists

# Setting up the histogram
sns.set_theme(style="ticks")
f, ax = plt.subplots(figsize=(10, 6))
sns.despine(f)

# Creating histogram
sns.histplot(
    data = data_scientist_df,
    x= 'basesalary',
    edgecolor=".3",
    linewidth=.5,
    binwidth= 20000
)

# Labeling Histogram
plt.title('Base Salary of Data Scientists')
plt.ylabel('Count')
plt.xlabel('Base Salary')
ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
ax.set_xticks([0, 50000, 100000, 150000, 200000, 250000, 300000, 400000, 500000, 600000, 700000])
plt.xticks(rotation=45)

# Looking at the histogram, there appears to be some outliers.

#%% We will now find and remove the ouliers from the data

q1 = data_scientist_df['basesalary'].quantile(0.25)
q3 = data_scientist_df['basesalary'].quantile(0.75)
iqr = q3 - q1

lower_bound = q1 - (1.5 * iqr)
upper_bound = q3 + (1.5 * iqr)

outliers = data_scientist_df[(data_scientist_df['basesalary'] < lower_bound) | (data_scientist_df['basesalary'] > upper_bound)]

data_scientist_no_outliers = data_scientist_df[~data_scientist_df.index.isin(outliers.index)]

#%% Drawing a histogram to see the shape of the base salary for data scientists without outliers

# Setting up the histogram
sns.set_theme(style="ticks")
f, ax = plt.subplots(figsize=(10, 6))
sns.despine(f)

# Creating histogram
sns.histplot(
    data = data_scientist_no_outliers,
    x= 'basesalary',
    edgecolor=".3",
    linewidth=.5,
    binwidth= 20000
)

# Labeling Histogram
plt.title('Base Salary of Data Scientists')
plt.ylabel('Count')
plt.xlabel('Base Salary')
ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
ax.set_xticks([25000, 50000, 75000, 100000, 125000, 150000, 175000, 200000, 225000, 250000])
plt.xticks(rotation=45)

#%% Creating a data frame grouped by location

# Finding the min, max, mean, median, and stand dev for the base salary for each location
ds_summary_by_location = data_scientist_no_outliers.groupby('location').agg(
     lowest_salary = ('basesalary', np.min),
     largest_salary = ('basesalary', np.max),
     avg_salary = ('basesalary', np.mean),
     median_salary = ('basesalary', np.median),
     std_salary = ('basesalary', np.std)).reset_index()

# Splitting the column 'location' into three columns ['City','State','Country']
ds_summary_by_location[['City','State','Country']] = ds_summary_by_location['location'].str.split(',',expand=True)

# Filling the na values with United States
ds_summary_by_location['Country'] = ds_summary_by_location['Country'].fillna('United States')

# Removing any country that is not United States
ds_summary_us = ds_summary_by_location[ds_summary_by_location['Country'] == 'United States']


#%% Data wrangling cost_of_living_df

# Renaming the column 'City' to 'Location'
cost_of_living_df = cost_of_living_df.rename(columns={'City': 'Location'})

# Splitting the column 'location' into three columns ['City','State','Country']
cost_of_living_df[['City','State','Country']] = cost_of_living_df['Location'].str.split(',',expand=True)

# Removing any country that is not United States
cost_of_living_us = cost_of_living_df[cost_of_living_df['Country'] == ' United States']

#%% Merging cost_of_living_us and ds_summary_us by City

# Data frame grouped by US cites and their corresponding cost of living
ds_cost_summary = ds_summary_us.merge(cost_of_living_us, how='inner', on='City')

# Dividing the average salary by the Cost of Living Plus Rent Index
ds_cost_summary['avg_salary_vs_cost'] = ds_cost_summary['avg_salary'] / ds_cost_summary['Cost of Living Plus Rent Index']

# Sorting the data frame to have the highest avg_salary_vs_cost at the top
ds_cost_summary = ds_cost_summary.sort_values(by='avg_salary_vs_cost', ascending=False)

# Finding the top 5 cities!!!
print(ds_cost_summary.iloc[0:5, 0])










