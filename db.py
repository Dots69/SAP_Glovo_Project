import mysql.connector
from config import DB_CONFIG

def connect():
    return mysql.connector.connect(**DB_CONFIG)

def register_user(username, password, role):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        db.commit()
        return True
    except:
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()

def login_user(username, password):
    db = connect()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user

def get_restaurants():
    db = connect()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM restaurants")
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

def get_menu(restaurant_id):
    db = connect()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu_items WHERE restaurant_id=%s", (restaurant_id,))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

def place_order(customer_id, restaurant_id, item_id, quantity):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO orders (customer_id, restaurant_id, item_id, quantity, status)
            VALUES (%s, %s, %s, %s, 'pending')
        """, (customer_id, restaurant_id, item_id, quantity))
        db.commit()
        return True, "Order placed"
    except:
        db.rollback()
        return False, "Error placing order"
    finally:
        cursor.close()
        db.close()

def get_courier_orders():
    db = connect()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE status='pending'")
    orders = cursor.fetchall()
    cursor.close()
    db.close()
    return orders

def complete_order(order_id, courier_id):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""
            UPDATE orders SET status='done', courier_id=%s WHERE id=%s
        """, (courier_id, order_id))
        db.commit()
        return True
    except:
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()

def add_restaurant(name, created_by):
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO restaurants (name, created_by) VALUES (%s, %s)", (name, created_by))
    db.commit()
    cursor.close()
    db.close()

def add_item(name, price, restaurant_id):
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO menu_items (name, price, restaurant_id) VALUES (%s, %s, %s)", (name, price, restaurant_id))
    db.commit()
    cursor.close()
    db.close()