# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.ion()
# Load data
orders_data =pd.read_excel('C:/Users/yugan/OneDrive/Desktop/Py course/Data/Source (Input) Data for the course/Ecommerce Orders Project/orders.xlsx')

#Load payments data

payments_data = pd.read_excel('C:/Users/yugan/OneDrive/Desktop/Py course/Data/Source (Input) Data for the course/Ecommerce Orders Project/order_payment.xlsx')

#Load customers data

customer_data = pd.read_excel('C:/Users/yugan/OneDrive/Desktop/Py course/Data/Source (Input) Data for the course/Ecommerce Orders Project/customers.xlsx')

# =============================================================================
# Describing the data
# =============================================================================

orders_data.info()
payments_data.info()
customer_data.info()

#Handling missing data

#Check for missing data in orders data

orders_data.isnull().sum()
payments_data.isnull().sum()
customer_data.isnull().sum()

#Filling in the missing values in orders data with a default value
orders_data2 = orders_data.fillna('N/A')

#Check for null values in orders_data2

orders_data2.isnull().sum()

#Drop rows with missing values in payments data
payments_data = payments_data.dropna()

#Check for null values in payments_data

payments_data.isnull().sum()

# =============================================================================
# Removing duplicate data
# =============================================================================

# Check for duplicates in orders_data

orders_data.duplicated().sum()

# Remove duplicates from orders data

orders_data = orders_data.drop_duplicates()

orders_data.duplicated().sum()

# Check for duplicates in payments_data

payments_data.duplicated().sum()

# Remove duplicates from orders data

payments_data = payments_data.drop_duplicates()

# =============================================================================
# Filtering the data
# =============================================================================

#Select a subset of orders data based on order status
invoiced_orders_data = orders_data[orders_data['order_status']=='invoiced']
#reset the index
invoiced_orders_data = invoiced_orders_data.reset_index(drop=True)

# Select a subset of the payments data where payment type = Credit Card and payment value > 1000
credit_card_payment_data = payments_data[
    (payments_data['payment_type'] == 'credit_card') & (payments_data['payment_value']>1000)]

# Select a subset of customers based on customer state = SP

state_sp_data = customer_data[customer_data['customer_state']=='SP']

# =============================================================================
# Merge and Join dataframes
# =============================================================================

#Merge orders data with payments data on order id column
merged_data = pd.merge(orders_data, payments_data, on='order_id')

#Join merged data with customer data on customer_id column

joined_data = pd.merge(merged_data,customer_data, on='customer_id')

# =============================================================================
# Data Visualization
# =============================================================================

#Create a field called month_year from order_purchase_timestamp
joined_data['month_year'] = joined_data['order_purchase_timestamp'].dt.to_period('M')
joined_data['week_year'] = joined_data['order_purchase_timestamp'].dt.to_period('W')
joined_data['year'] = joined_data['order_purchase_timestamp'].dt.to_period('Y')

grouped_data = joined_data.groupby('month_year')['payment_value'].sum()
grouped_data = grouped_data.reset_index()

#convert month_year from period to string
grouped_data['month_year'] = grouped_data['month_year'].astype(str)
#creating plot

plt.plot(grouped_data['month_year'], grouped_data['payment_value'],color ='red',marker ='o')
plt.ticklabel_format(useOffset=False, style='plain', axis ='y')
plt.xlabel('Month and Year')
plt.ylabel('Payment value')
plt.title('Payment value by Month and year')
plt.xticks(rotation = 90)
plt.show()

#Scatted plot

#Create dataframe
scatter_df = joined_data.groupby('customer_unique_id').agg({'payment_value':'sum', 'payment_installments': 'sum'})

plt.scatter(scatter_df['payment_value'],scatter_df['payment_installments'])
plt.xlabel('Payment Value')
plt.ylabel('Payment Installments')
plt.title('Payment value vs Installments')
plt.show()

# Using seaborn to create scatter plot
sns.set_theme(style='darkgrid')
sns.scatterplot(data=scatter_df,x='payment_value',y='payment_installments')
plt.xlabel('Payment Value')
plt.ylabel('Payment Installments')
plt.title('Payment value vs Installments')
plt.show()

# Creating bar chart
bar_chart_df = joined_data.groupby(['payment_type', 'month_year'])['payment_value'].sum()
bar_chart_df = bar_chart_df.reset_index()
pivot_data = bar_chart_df.pivot(index='month_year', columns='payment_type', values='payment_value')

pivot_data.plot(kind='bar', stacked='True')
plt.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.xlabel('Month of Payment')
plt.ylabel('Payment Value')
plt.title('Payment per payment value by month')
plt.show()

#Creating a box plot

payment_values = joined_data['payment_value']
payment_types = joined_data['payment_type']

#Creating box plot as per payment type
plt.boxplot([payment_values[payment_types =='credit_card'],
             payment_values[payment_types =='boleto'],
             payment_values[payment_types =='voucher'],
             payment_values[payment_types =='debit_card']],
            labels = ['Credit Card', 'Boleto', 'Voucher', 'Debit Card']
            )
plt.xlabel('Payment Type')
plt.ylabel('Payment Value')
plt.show()

#Creating a subplot (3 plots in one)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10,10))

#ax1 is box plot

ax1.boxplot([payment_values[payment_types =='credit_card'],
             payment_values[payment_types =='boleto'],
             payment_values[payment_types =='voucher'],
             payment_values[payment_types =='debit_card']],
            labels = ['Credit Card', 'Boleto', 'Voucher', 'Debit Card']
            )
ax1.set_xlabel('Payment Type')
ax1.set_ylabel('Payment Value')


#ax2 is stacked barchart

pivot_data.plot(kind='bar', stacked='True', ax=ax2)
ax2.ticklabel_format(useOffset=False, style='plain', axis='y')
ax2.set_xlabel('Month of Payment')
ax2.set_ylabel('Payment Value')
ax2.set_title('Payment per payment value by month')

#ax3 is scatter plot

ax3.scatter(scatter_df['payment_value'],scatter_df['payment_installments'])
ax3.set_xlabel('Payment Value')
ax3.set_ylabel('Payment Installments')
ax3.set_title('Payment value vs Installments')
fig.tight_layout()
plt.show()





















































