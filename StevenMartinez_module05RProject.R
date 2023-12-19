library(ggplot2)
library(dplyr)
library(tidyr)
library(scales)


# Importing Data ----------------------------------------------------------


data_scientist_df2 <- read.csv("R Project/Data/r_project_data.csv",
                              stringsAsFactors = FALSE) %>%
  select(-X)

View(data_scientist_df)

# Data frame with just full time employees
ft_employees <- filter(data_scientist_df, employment_type == 'FT')


# Salaries of Data Scientists over the last two years ------------------------------------------------


# Full Time average salary by year
avg_salary_by_year_FT <- ft_employees %>%
  group_by(work_year) %>%
  summarize(salary_in_usd = mean(salary_in_usd))

avg_salary_by_year_FT


# Line plot showing the average salaries of full time data scientists over the years
avg_salary_by_year_FT %>%
  ggplot() +
  geom_line(aes(x = work_year, y = salary_in_usd), color = 'blue') +
  labs(x = 'Year',
       y = 'Salary in USD',
       title = 'Average Salary of Full Time Data Scientist over the Years') +
  scale_y_continuous(labels = comma) +
  theme_minimal() +
  ggeasy::easy_center_title()

# The average of a full time data scientist is increasing rapidly year by year.
# It is crucial to start a data science team now before salaries increase even more.


# Average salary of full time DS by experience and a bar plot for visualization ------------------------


# Average salary(in USD) by experience and employment type
avg_salary_by_experience_FT <- ft_employees %>%
  group_by(experience_level) %>%
  summarize(salary_in_usd = mean(salary_in_usd))

avg_salary_by_experience_FT


# Plot comparing the salaries based on experience and employment type
avg_salary_by_experience_FT %>%
  ggplot() +
  geom_col(aes(x = experience_level, y = salary_in_usd, fill = experience_level)) +
  labs(x = 'Experience Level',
       y = 'Salary in USD',
       title = 'Average Salary of Full Time Data Scientist by Experience') +
  scale_y_continuous(labels = comma) +
  theme_minimal() +
  theme(legend.position = 'none') +
  ggeasy::easy_center_title()

# The ideal candidate would be either senior-level or executive-level 
# because they will help with grow and lead a team in the future.


# Offshore vs US ----------------------------------------------------------


# Offshore residence salaries grouped by experience level
offshore_avg_salary_by_experience <- ft_employees %>%
  filter(employee_residence != 'US') %>%
  group_by(experience_level) %>%
  summarize(salary_in_usd = mean(salary_in_usd))

offshore_avg_salary_by_experience


# US residence salaries grouped by experience
us_avg_salary_by_experience <- ft_employees %>%
  filter(employee_residence == 'US') %>%
  group_by(experience_level) %>%
  summarize(salary_in_usd = mean(salary_in_usd))

us_avg_salary_by_experience


# Offshore vs US avg salaries
offshore_vs_us_avg_salary <- offshore_avg_salary_by_experience %>%
  inner_join(us_avg_salary_by_experience, by='experience_level') %>%
  rename(offshore_salary = 2, us_salary = 3)

offshore_vs_us_avg_salary


# Percentage difference between offshore and US salaries by experience.
offshore_vs_us_avg_salary %>%
  group_by(experience_level) %>%
  reframe(salary_difference_percentage = (offshore_salary / us_salary))


# It seems the best option is to hire offshore. Hiring offshore will cut down cost significantly.


# Below are the graphs of offshore and US average salaries but I don't think I will be using them.
# The offshore_vs_us_avg_salary data frame does a good job comparing the salaries.

# Offshore residence average salary plot by experience level
offshore_avg_salary_by_experience %>%
  ggplot() +
  geom_col(aes(x = experience_level, y = salary_in_usd, fill = experience_level)) +
  labs(x = 'Experience Level',
       y = 'Salary in USD',
       title = 'Average Salary of Full Time Data Scientist by Experience') +
  scale_y_continuous(labels = comma) +
  theme_minimal() +
  theme(legend.position = 'none') +
  ggeasy::easy_center_title()


# US residence average salary plot by experience level
us_avg_salary_by_experience %>%
  ggplot() +
  geom_col(aes(x = experience_level, y = salary_in_usd, fill = experience_level)) +
  labs(x = 'Experience Level',
       y = 'Salary in USD',
       title = 'Average Salary of Full Time Data Scientist by Experience') +
  scale_y_continuous(labels = comma) +
  theme_minimal() +
  theme(legend.position = 'none') +
  ggeasy::easy_center_title()


# Hiring Recommendation ----------------------------------------------

# Recommendation will be to hire an offshore data scientist with executive experience

# Average salary of an offshore DS with Executive experience at a medium size company
filter(ft_employees, company_size == 'M', experience_level == 'EX', employee_residence != 'US') %>%
  summarize(salary_in_usd = mean(salary_in_usd))


# Average salary of a US residence DS with Executive experience at a medium size company
filter(ft_employees, company_size == 'M', experience_level == 'EX', employee_residence == 'US') %>%
  summarize(salary_in_usd = mean(salary_in_usd))


# Based on the average salary of an offshore and US residence data scientists with executive experience,
# the salary range should be between 108,000 to 193,000.
# This range varies according to the data scientist residence location.
