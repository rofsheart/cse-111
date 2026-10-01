import csv
import random
from datetime import datetime, timedelta

Store_name = "Hearton Store"
Tax_rate = 0.06


def read-dictionary(filename, key_column_index): 
""",,,"""
    dictionary = {}
    with open(filename, "rt") as csv_file:
        reader = csv.reader(csv_file)
        next(reader) 
        for row in reader:
            if len(row) == 0:
                continue
            key = row[key_column_index]
            dictionary[key] = row
    return dictionary


def main():
    try:
        products_dict = read-dictionary("products.csv", 0)
        
        print(Store_name)

        total_items = 0
        subtotal = 0.0
        ordered_name = []

        with open("requests.csv", "rt") as requests_file:
            reader = csv.reader(requests_file)
            next(reader) 
            for row in reader:
                if len(row) == 0:
                    continue
                product_number = row[0]
                quantity = int(row[1])
                product_info = products_dict.get(product_number)
                product_name = product_info[1]
                price = float(product_info[2])
                print(f"{product_name}: {quantity} @ {price})
                total_items += quantity
                subtotal += quantity * price
                ordered_name.append(product_name)

        sales_tax = subtotal * Tax_rate
        total = subtotal + sales_tax