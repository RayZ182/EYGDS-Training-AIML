import pandas as pd
from datetime import datetime

products_df = pd.read_csv('products.csv')
customers_df = pd.read_csv('customers.csv')
orders_df = pd.read_csv('orders.csv')

# joining datasets
order_cust = pd.merge(orders_df, customers_df, on = 'CustomerID')
df = pd.merge(order_cust, products_df, on = 'ProductID')

# Add new column
df['TotalAmount'] = df['Quantity'] * df['Price']

# extract month
df['OrderMonth'] = pd.to_datetime(df['OrderDate']).dt.month_name()

# Remove Orders with quantity < 2
df = df[df['Quantity'] >= 2]

# Only India and UAE
df = df[(df['Country'] == 'UAE') | (df['Country'] == 'India')]

# Category Summary
category_df = df.groupby('Category')['TotalAmount'].sum().reset_index()

# Segment Summary
segment_df = df.groupby('Segment')['TotalAmount'].sum().reset_index()

# Sorting customers
df = df.sort_values(by = "TotalAmount", ascending = False)

# LOADING
df.to_csv('processed_orders.csv', index=False)
category_df.to_csv('category_summary.csv', index=False)
segment_df.to_csv('segment_summary.csv', index=False)

