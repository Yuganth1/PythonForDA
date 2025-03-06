# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 10:09:07 2025

@author: yugan
"""

#Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Load datasets
loan_data = pd.read_excel('C:/Users/yugan/OneDrive/Desktop/Py course/Data/Source (Input) Data for the course/Loan Analysis Project/loandataset.xlsx')
customer_data = pd.read_csv('C:/Users/yugan/OneDrive/Desktop/Py course/Data/Source (Input) Data for the course/Loan Analysis Project/customer_data.csv', sep=';')

#Display first few rows of dataset
loan_data.head()
customer_data.head()

#Merging two dataframes on ID

complete_data = pd.merge(loan_data,customer_data, left_on='customerid', right_on='id')

#Check for missing data
complete_data.isnull().sum()

#Remove rows with missing data
complete_data = complete_data.dropna()

#Check for duplicated data
complete_data.duplicated().sum()

#Define a function to categorize purpose

def categorize_purpose(purpose):
    if purpose in ['credit_card','debt_consolidation']:
        return 'Financial'
    elif purpose in ['educational', 'small business']:
        return 'Educational/Business'
    else:
        return 'Other'

categorize_purpose('credit_card')
complete_data['purpose_category'] = complete_data['purpose'].apply(categorize_purpose)

#Create a new function based on criteria
#If dti > 20 and delinq.2years >2 and the revol.util> 60 then borrower is high risk

def assess_risk(row):
    if row['dti'] > 20 and row['delinq.2yrs'] > 2 and row['revol.util'] > 60:
        return 'High Risk'
    else:
        return 'Low Risk'
    
complete_data['Risk'] = complete_data.apply(assess_risk, axis=1)

#Create new function to categorize FICO scores

def categorize_fico(fico_score):
    if fico_score >= 800 & fico_score<=850:
        return "Excellent"
    elif fico_score >= 740 and fico_score <800:
        return "Very Good"
    elif fico_score >= 670 and fico_score < 740:
        return "Good"
    elif fico_score >= 580 and fico_score < 670:
        return "Fair"
    else:
        return "Poor"
    
complete_data['fico_category'] = complete_data['fico'].apply(categorize_fico)

#Identify customers with more than average inquiries and derogatory records 

def identify_high_inq_derog(row):
    average_inq = complete_data['inq.last.6mths'].mean()
    average_derog = complete_data['pub.rec'].mean()
    
    if row['inq.last.6mths'] > average_inq and row['pub.rec'] > average_derog:
        return True
    else:
        return False
    
complete_data['High_Inquiries_and_publicrecords'] = complete_data.apply(identify_high_inq_derog, axis=1)

#Data Visualization
#Set style of visualization
sns.set_style('darkgrid')
#Bar chart to show distribution of loan by purpose

plt.figure(figsize=(10,6))
sns.countplot(x= 'purpose',data = complete_data, palette='dark')
plt.title('Loan-Purpose distribution')
plt.xlabel('Purpose of loan')
plt.ylabel('Number of loans')
plt.xticks(rotation=45)
plt.show()

#Create scatterplot for dti vs income

plt.figure(figsize=(10,6))
sns.scatterplot(x= 'log.annual.inc', y= 'dti', data = complete_data)
plt.title('Debt-to-income ratio vs Annual income')
plt.show()

#Distribution of fico scores
plt.figure(figsize=(10,6))
sns.histplot(complete_data['fico'], bins=30, kde=True)
plt.title('Distribution of FICO scores')
plt.show()

#Box plot to determine risk vs interest rate

plt.figure(figsize=(10,6))
sns.boxplot(x= 'Risk', y='int.rate', data= complete_data)
plt.title('Interest rate vs risk')
plt.show()

#Subplots

fig, axs = plt.subplots(2,2,figsize=(20,20))

# 1. Loan Purpose Distribution
sns.countplot(x='purpose',data = complete_data, ax=axs[0,0])
axs[0,0].set_title('Loan Purpose Distribution')
plt.setp(axs[0,0].xaxis.get_majorticklabels(), rotation=45)

# 2. Debt-to-income ratio vs FICO score
sns.scatterplot(x='fico', y='dti', data= complete_data, ax=axs[0,1])
axs[0,1].set_title('Debt-to-income ratio vs FICO score')

# 3. Distribution of FICO scores
sns.histplot(complete_data['fico'], bins=30, ax=axs[1,0])
axs[1,0].set_title('Distribution of FICO scores')

# 4. Risk category vs Interest rate
sns.boxplot(x='Risk',y='int.rate',data = complete_data, ax=axs[1,1])
axs[1,1].set_title('Interest Rate vs Risk Category')

#Adjust layout
plt.tight_layout()
plt.show()




























