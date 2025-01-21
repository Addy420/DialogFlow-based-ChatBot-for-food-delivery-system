import mysql.connector

# Establishing a connection to the MySQL database
global cnx
cnx = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="root",
    database="jaldiram_eatery"
)

# Function to insert an order item into the database
def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        # Calling the stored procedure to insert the order item
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        # Committing the changes
        cnx.commit()

        # Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1

# Function to insert a record into the order_tracking table
def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    cnx.commit()

    # Closing the cursor
    cursor.close()

# Function to get the total price of an order from the database
def get_total_order_price(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    return result

# Function to get the next available order ID
def get_next_order_id():
    cursor = cnx.cursor()

    # Executing the SQL query to get the next available order ID
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    # Returning the next available order ID
    if result is None:
        return 1
    else:
        return result + 1

# Function to fetch the order status from the database
def get_order_status(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order status
    query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()

    # Closing the cursor
    cursor.close()

    # Returning the order status
    if result:
        return result[0]
    else:
        return None

# Function to fetch the details of an order from the database
def get_order_details(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order details
    query = f"""
        SELECT f.name AS food_item, o.quantity 
        FROM orders o
        JOIN food_items f ON o.item_id = f.item_id
        WHERE o.order_id = {order_id}
    """
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchall()

    # Closing the cursor
    cursor.close()

    # Returning the order details
    return result

# Example usage if executed as a standalone script
if __name__ == "__main__":
    print(get_next_order_id())  # Example usage to get the next available order ID

