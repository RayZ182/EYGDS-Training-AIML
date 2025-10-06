import logging
import pandas as pd

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    filename = 'sales.log',
                    level = logging.DEBUG)

try:
    # read the data
    df = pd.read_csv('products_ey.csv')
    print(df.head())

    # total sales of each item
    for index, row in df.iterrows():
        product = row['product']
        price = row['price']
        quantity = row['quantity']

        total_sales = price * quantity
        print(f" {product} = {total_sales}")
        logging.info(f" {product} = {total_sales}")

except FileNotFoundError as e:
    logging.error("File not found")
    print("File not found")

except TypeError as e:
    logging.error("Invalid Numerical value")
    print("Invalid Numerical value")