import mysql.connector
from mysql.connector import Error
import datetime
from decimal import Decimal

# List of special discounts (converted to Decimal)
special_discounts = [Decimal('0.1'), Decimal('0.2'), Decimal('0.15'), Decimal('0.25')]

# Dictionary of item categories
item_categories = {
    "foods": "Food Items",
    "drinks": "Drink Items",
    "services": "Other Services"
}


# Base class for items
class Item:
    def __init__(self, item_id, name, price):
        self.item_id = item_id
        self.name = name
        self.price = Decimal(price)  # Convert price to Decimal

    def display(self):
        return f"{self.item_id}. {self.name} - RM {self.price}"


# Specific class for foods, inheriting from Item
class Food(Item):
    def __init__(self, item_id, name, price):
        super().__init__(item_id, name, price)


# Specific class for drinks, inheriting from Item
class Drink(Item):
    def __init__(self, item_id, name, price):
        super().__init__(item_id, name, price)


# Specific class for services, inheriting from Item
class Service(Item):
    def __init__(self, item_id, name, price):
        super().__init__(item_id, name, price)


# Function to establish a connection to the MySQL database
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshitha11@1999",
            database="my_restaurant_db"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# Function to fetch data from the database
def fetch_data(connection, table_name, item_class):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()

        items = [item_class(*item) for item in data]
        return items
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()


# Function to display menu items from the database using List comprehension
def display_menu(connection, table_name, item_class=Item):  # Provide a default value for item_class
    items = fetch_data(connection, table_name, item_class)
    if items:
        print(f"\nMenu ({item_categories.get(table_name, table_name)}):")
        [print(item.display()) for item in items]
    else:
        print(f"Error fetching data from {table_name}")


# Function to handle generating reports with special discounts
def generate_report(connection):
    try:
        cursor = connection.cursor()

        # Get the current date
        current_date = datetime.datetime.now().date()

        # Execute a query to get orders placed on the current date
        cursor.execute("SELECT item_type, item_id, SUM(quantity) FROM orders "
                       "GROUP BY item_type, item_id")
        orders = cursor.fetchall()

        report = "\n\n\n" + " " * 17 + "*" * 35 + "\n" + " " * 17 + "DATE: " + str(datetime.datetime.now())[
                                                                               :19] + "\n" + " " * 17 + "-" * 35

        total_price = 0

        for order in orders:
            cursor.execute(f"SELECT name, price FROM {order[0]} WHERE id = {order[1]}")
            item = cursor.fetchone()
            if item:
                item_name = item[0]
                quantity = order[2]
                item_price = item[1]

                # Apply discounts based on your logic here
                # For example, check if the item_type is eligible for a discount
                if order[0] in item_categories and item_categories[order[0]] == "Food Items":
                    # Apply a special discount for food items
                    item_price *= (1 - special_discounts[0])

                total_price += quantity * item_price
                report += f"\n{item_name} - {quantity} x RM {item_price}"

        report += "\n" + " " * 17 + "-" * 35 + "\n" \
                                               "" + " " * 17 + f"TOTAL PRICES:       RM {round(total_price, 2)}" + "\n" + " " * 17 + "*" * 35

        print(report)

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()


# Function to handle processing payments
def process_payment(connection):
    try:
        generate_report(connection)
        print("\n (P) PAY           (M) MAIN MENU           (E) EXIT\n" + "_" * 72)
        input_1 = str(input("Please Select Your Operation: ")).upper()

        if input_1 == 'P':
            print("\n" * 10)
            print("Successfully Paid!")
        elif input_1 == 'M':
            print("\n" * 10)
            main_menu(connection)
        elif input_1 == 'E':
            print("*" * 32 + "THANK YOU" + "*" * 31 + "\n")
        else:
            print("\n" * 10 + f"ERROR: Invalid Input ({input_1}). Try again!")

    except Error as e:
        print(f"Error: {e}")


# Function to handle ordering other services
def order_other_services(connection):
    try:
        print("Order Other Services:")
        display_menu(connection, "services", Service)

        service_id = input("Enter the ID of the service you want to order: ")
        quantity = int(input("Enter the quantity: "))

        # Perform the logic to place the order for the selected service
        # You can add this logic based on your database schema and requirements

        print(f"\nOrder placed for service with ID {service_id} - Quantity: {quantity}")

    except ValueError:
        print("Invalid input for quantity. Please enter a valid integer.")


# Function to handle ordering food and drinks
def order_food_drink(connection):
    try:
        print("Order Food and Drinks:")
        display_menu(connection, "foods", Food)
        display_menu(connection, "drinks", Drink)

        food_id = input("Enter the ID of the food item you want to order: ")
        drink_id = input("Enter the ID of the drink item you want to order: ")
        food_quantity = int(input("Enter the quantity of the food item: "))
        drink_quantity = int(input("Enter the quantity of the drink item: "))

        # Perform the logic to place the order for the selected food and drink items
        # You can add this logic based on your database schema and requirements

        print(f"\nOrder placed for food with ID {food_id} - Quantity: {food_quantity}")
        print(f"Order placed for drink with ID {drink_id} - Quantity: {drink_quantity}")

    except ValueError:
        print("Invalid input for quantity. Please enter a valid integer.")


# Main menu function
def main_menu(connection):
    while True:
        print("*" * 31 + "MAIN MENU" + "*" * 32 + "\n"
                                                  "\t(O) ORDER\n"
                                                  "\t(R) REPORT\n"
                                                  "\t(P) PAYMENT\n"
                                                  "\t(S) SERVICES\n"  # Added option for services
                                                  "\t(E) EXIT\n" + "_" * 72)

        choice = input("Please Select Your Operation: ").upper()

        if choice == 'O':
            print("\n" * 10)
            order_food_drink(connection)
        elif choice == 'R':
            print("\n" * 10)
            generate_report(connection)
        elif choice == 'P':
            print("\n" * 10)
            process_payment(connection)
        elif choice == 'S':  # Added case for services
            print("\n" * 10)
            order_other_services(connection)
        elif choice == 'E':
            print("*" * 32 + "THANK YOU" + "*" * 31 + "\n")
            break
        else:
            print("\n" * 10 + f"ERROR: Invalid Input ({choice}). Try again!")


# Main program
connection = create_connection()

if connection:
    display_menu(connection, "foods")
    display_menu(connection, "drinks")
    display_menu(connection, "services")

    main_menu(connection)

    # Close the connection when done
    connection.close()
