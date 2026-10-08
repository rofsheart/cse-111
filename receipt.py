import csv
from datetime import datetime

def read_dictionary(filename, key_column_index):
    """
    Reads a CSV file and returns a dictionary.
    The key is the value in the column indicated by key_column_index.
    The value is the entire row as a list.
    """
    dictionary = {}
    with open(filename, "r", newline="") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if len(row) == 0:
                continue
            key = row[key_column_index]
            dictionary[key] = row
    return dictionary


def main():
    try:
        # Read the product catalog into a dictionary
        products_dict = read_dictionary("products.csv", 0)

        # Display the dictionar
        print("Products dictionary:")
        print(products_dict)
        print()

        # Store name
        store_name = "Uncle's Grocery Store"
        print(store_name)
        print()

        total_items = 0
        subtotal = 0.0

        # customer's order file
        with open("request.csv", "r", newline="") as request_file:
            reader = csv.reader(request_file)
            next(reader)  # skip the header row

            for row in reader:
                if len(row) == 0:
                    continue

                product_number = row[0]
                quantity = int(row[1])

                # Look up the product
                product = products_dict[product_number]
                product_name = product[1]
                price = float(product[2])

                # Print item details
                print(f"{product_name}: {quantity} @ {price:.2f}")

                total_items += quantity
                subtotal += quantity * price

        # Calculate sales tax and total
        sales_tax = subtotal * 0.06
        total = subtotal + sales_tax

        # Print totals
        print()
        print(f"Number of items: {total_items}")
        print(f"Subtotal: {subtotal:.2f}")
        print(f"Sales tax: {sales_tax:.2f}")
        print(f"Total: {total:.2f}")
        print()

        # Thank you message
        print("Thank you for shopping with us!")

        # Current date and time
        now = datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))

    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
    except PermissionError as e:
        print(f"Error: Permission denied - {e.filename}")
    except KeyError as e:
        print(f"Error: Product not found in catalog - {e}")


if __name__ == "__main__":
    main()
