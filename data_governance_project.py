#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:06:51 2023

@author: stevenmartinez
"""

#%% Libraries

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

import os
os.getcwd()

#%% Importing the data

merr_customer_df = pd.read_excel('/Users/stevenmartinez/Documents/Merrimack Classes/Data Governance and Privacy/Data/Merr.Customer.Survey.xlsx')

merr_customer_df.dtypes
merr_customer_df.shape


merr_customer_df.nunique()
merr_customer_df.describe()


#%% First Variable - Gender

# The gender is masked in the data set. 1s are males and 0s are females

# Creating a data frame to count how many male and females there are in the data set
gender_counts = merr_customer_df.value_counts('Gender').reset_index()

gender_counts.loc[gender_counts['Gender'] == 1] # There are 2518 males
gender_counts.loc[gender_counts['Gender'] == 0] # There are 2482 females


#%% Second variable - Age

# Looking at how many different ages the data set has
merr_customer_df['Age'].nunique()   # There are 62 different ages
merr_customer_df['Age'].min()       # Youngest in data set is 18
merr_customer_df['Age'].max()       # Oldest in data set is 79

# Creating a data frame to count how many times a value in Age appears in the data set
age_counts = merr_customer_df.value_counts('Age').reset_index()

# Looking at age counts, there are 62 unique ages and the minimum an age appears is 58
age_counts['count'].min() # Lowest occurance is 58
age_counts.loc[age_counts['count'] == 58] # 76 Years old

# Age does not have to be changed. It will already pass the 1/3 threshold.
# However, we will change it to a range of ages to reduce the amount of equivalence classes.



# Looking at how many different education years are in the data set
merr_customer_df['EducationYears'].nunique()    # There are 18 different education years

# Creating a data frame to count how many times a value in EducationYears appears in the data set
education_years_counts = merr_customer_df.value_counts('EducationYears').reset_index()

# Looking at education years counts, the lowest occurance is 4, for 23 education years
education_years_counts['count'].min()  # Lowest occurance is 4 
education_years_counts.loc[education_years_counts['count'] == 4] # 23 education years

# Education years does not have to be changed. It will pass the 1/3 threshold

#%% Third Variable - HomeOwner

# The HomeOwner is masked in the data set. 1s are home owners and 0s are not

# Creating a data frame to count how many homeowners there are in the data set
homeowner_counts = merr_customer_df.value_counts('HomeOwner').reset_index()

homeowner_counts.loc[homeowner_counts['HomeOwner'] == 1] # There are 3148 homeowners
homeowner_counts.loc[homeowner_counts['HomeOwner'] == 0] # There are 1852 who are not


#%% Fourth Variable - LoanDefault

# The LoanDefault is masked in the data set. 1s have a loand default and 0s do not

# Creating a data frame to count how many customers have a loan default in the data set
loandefault_counts = merr_customer_df.value_counts('LoanDefault').reset_index()

loandefault_counts.loc[loandefault_counts['LoanDefault'] == 1] # There are 1171 customers who have a loan default
loandefault_counts.loc[loandefault_counts['LoanDefault'] == 0] # There are 3829 who have not


#%% New data frame with only four columns -> Gender, Age, HouseholdIncome, CreditDebt

# New data frame with the variables we are interested in and need to de-identified
quasi_df = merr_customer_df[['Gender', 'Age', 'HomeOwner', 'LoanDefault']].copy()

print(quasi_df)


#%% Changing Age to a range of values

# Defining a function to convert values to range strings for Age
def int_to_range_age(value):
    ranges = [(18, 29), (30, 39), (40, 49), (50, 59), (60, 69), (70, 79)]
    for start, end in ranges:
        if start <= value <= end:
            return f'{start}-{end}'
        
# Converting Age to a range of values
quasi_df['Age'] = (quasi_df['Age'].apply(int_to_range_age))

# Counting how many observations are in each equivalence class
quasi_df.loc[quasi_df['Age'] == '18-29']    # There are 1074 observations
quasi_df.loc[quasi_df['Age'] == '30-39']    # There are 882 observations
quasi_df.loc[quasi_df['Age'] == '40-49']    # There are 781 observations
quasi_df.loc[quasi_df['Age'] == '50-59']    # There are 802 observations
quasi_df.loc[quasi_df['Age'] == '60-69']    # There are 796 observations
quasi_df.loc[quasi_df['Age'] == '70-79']    # There are 665 observations



#%% Counting how many equivalence classes there are and how many observations in each equivalence class


# Create an empty dictionary to store equivalence classes
quasi_equivalence_classes = {}

# Group the DataFrame by unique combinations of the four columns
for index, row in quasi_df.iterrows():
    key = (row['Gender'], row['Age'], row['HomeOwner'], row['LoanDefault'])
    
    if key not in quasi_equivalence_classes:
        quasi_equivalence_classes[key] = []
    
    quasi_equivalence_classes[key].append(index)

# There are 48 total equivalence classes.


#Creating a data frame for the size of the equivalence classes
data = {
    'Gender': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'Age': ['18-29', '18-29', '18-29', '18-29', '30-39', '30-39', '30-39', '30-39', '40-49', '40-49', '40-49', '40-49', '50-59', '50-59', '50-59', '50-59', '60-69', '60-69', '60-69', '60-69', '70-79', '70-79', '70-79', '70-79', '18-29', '18-29', '18-29', '18-29', '30-39', '30-39', '30-39', '30-39', '40-49', '40-49', '40-49', '40-49', '50-59', '50-59', '50-59', '50-59', '60-69', '60-69', '60-69', '60-69', '70-79', '70-79', '70-79', '70-79'],
    'HomeOwner': [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    'LoanDefault': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    'Equivalence_Size': [90, 120, 171, 156, 100, 45, 179, 78, 112, 33, 217, 48, 116, 21, 216, 41, 137, 16, 246, 15, 131, 6, 184, 4, 101, 116, 170, 150, 114, 54, 201, 111, 93, 20, 211, 47, 117, 14, 245, 32, 127, 13, 218, 24, 152, 4, 181, 3]
}

risk_df = pd.DataFrame(data)

# Calculating the P(re-id | attempt) and adding the column to the risk_df
risk_df['P(re-id | attempt)'] = (1 / risk_df['Equivalence_Size'])

#%% Scenario 1 Deliberate Data Attack

# We are goign to assume that 20% of the company employees may go rogue.
# We are calculating the risk for each equivalence class using 20% for the P(attempt)
# Scenario 1 risk
risk_df['Scenario1'] = (risk_df['P(re-id | attempt)']) * 0.2

# max risk for scenario 1
print(risk_df['Scenario1'].max())


#%% Scenario 2 Inadvert Data Attack

# We are going to assume that we work for Verizon. 
# In order to find the prevelance number, we are going to use the number of U.S. subscribers Verizon has out of the total
# U.S. population that has a wireless provider.

# From the big 4 wireless providers, Verizon has 143.3 million subscribers out of 496.83 million
prevelance_number = 143.3 / 496.83
print(prevelance_number)

# We will now calculate the probability of an acquintance
acquintance = 1 - (1 - prevelance_number)**150
print(acquintance)

# Scenario 2 risk
risk_df['Scenario2'] = (risk_df['P(re-id | attempt)']) * acquintance

# max risk for scenario 2
print(risk_df['Scenario2'].max())


#%% Scenario 3 Data Breach

# Through my research, I have found that 45% of US companies have experienced a data breach.
# This is based on various websites confirming the same information.
# Therefore, we will use 45% as the probability of breach.

# Scenario 3 risk
risk_df['Scenario3'] = (risk_df['P(re-id | attempt)']) * 0.45

# max risk for scenario 3
print(risk_df['Scenario3'].max())


#%% Scenario 4 Demonstration Attack

# Scenario 4 risk
risk_df['Scenario4'] = (1 / risk_df['Equivalence_Size'])

# max risk for scenario 4
print(risk_df['Scenario4'].max())

#%% median risk

# median risk is calculated by number of equivalence classes divided by number of records
median_risk = 48 / 5000
print(median_risk)

#%% Results Diagnostics

print((risk_df['Scenario1'] < 0.05).sum())  # 4989 / 5000
print((risk_df['Scenario1'] < 0.10).sum())  # 5000 / 5000

print((risk_df['Scenario2'] < 0.05).sum())  # 4905 / 5000
print((risk_df['Scenario2'] < 0.10).sum())  #  4983 / 5000
print((risk_df['Scenario2'] < 0.20).sum())  # 4989 / 5000
print((risk_df['Scenario2'] <= 0.33333).sum())  # 5000 / 5000

print((risk_df['Scenario3'] < 0.05).sum())  # 4983 / 5000
print((risk_df['Scenario3'] < 0.10).sum())  # 4989 / 5000
print((risk_df['Scenario3'] < 0.20).sum())  # 5000 / 5000

print((risk_df['Scenario4'] < 0.05).sum())  # 4905 / 5000
print((risk_df['Scenario4'] < 0.10).sum())  # 4983 / 5000
print((risk_df['Scenario4'] < 0.20).sum())  # 4989 / 5000
print((risk_df['Scenario4'] <= 0.3333333).sum())  # 5000 / 5000







