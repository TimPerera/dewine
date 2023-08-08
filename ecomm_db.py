import sqlite3
import Faker

# create table
connection = sqlite3.connect('voila.db')

cursor = connection.cursor()

create_table_query = ["""
    CREATE TABLE IF NOT EXISTS customer (
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL,
        scene_ID INTEGER PRIMARY KEY
        )

""",
"""
    CREATE TABLE IF NOT EXISTS credentials (
        credentials_id INTEGER PRIMARY KEY,
        scene_ID INTEGER,
        password_hash TEXT,
        )
""",
"""
    CREATE TABLE IF NOT EXISTS customerLocation (
        address_id INTEGER PRIMARY KEY, 
        scene_ID INTEGER,
        full_address TEXT, 
        city TEXT,
        postal_code TEXT
    )
""",
"""
    CREATE TABLE IF NOT EXISTS contact (
        contact_id INTEGER PRIMARY KEY,
        scene_ID INTEGER,
        email TEXT NOT NULL UNIQUE,
        phone INTEGER NOT NULL UNIQUE,
        address_id INTEGER
    )
""",
"""
    CREATE TABLE IF NOT EXISTS creditCardPayment (
        card_id INTEGER PRIMARY KEY, 
        card_number INTEGER NOT NULL, 
        card_expiry DATE NOT NULL,
        store_credit REAL
    )
""",
"""
    CREATE TABLE IF NOT EXISTS orderTable (
        order_id INTEGER PRIMARY KEY,
        scheduledDeliveryDatetime DATETIME, 
        deliveryLocation TEXT,
        scene_ID INTEGER,
        orderDetails_id INTEGER, 
        shoppingCart_id INTEGER,
        session_id INTEGER,
        orderStatus_id INTEGER,
        payment_id INTEGER
    )
""",
"""
    CREATE TABLE IF NOT EXISTS scenePlus (
        scene_ID INTEGER PRIMARY KEY,
        scene_ID INTEGER,
        points REAL,
    )
""",
"""
    CREATE TABLE IF NOT EXISTS payment (
        payment_id INTEGER PRIMARY KEY,
        datetime DATETIME NOT NULL,
        amount FLOAT NOT NULL,
        card_id INTEGER,
        order_id INTEGER
    )
""",
"""
    CREATE TABLE IF NOT EXISTS orderDetails(
        orderDetails_id INTEGER PRIMARY KEY, 
        order_id INTEGER,
        product_id INTEGER,
        discount REAL
    )
""",
"""
    CREATE TABLE IF NOT EXISTS orderStatus (
        orderStatus_id INTEGER PRIMARY KEY, 
        orderStatus TEXT NOT NULL, 
        statusDate DATE NOT NULL, 
        gpsCoord REAL,
        order_id INTEGER
    )
""",
"""
    CREATE TABLE IF NOT EXISTS session (
        session_id INTEGER PRIMARY KEY,
        created_at DATETIME,
        ended_at DATETIME,
        sessionTime TIME,
        scene_ID INTEGER
    )
""",
"""
    CREATE TABLE IF NOT EXISTS shoppingCart (
        shoppingCart_id INTEGER PRIMARY KEY,
        quantity INTEGER NOT NULL,
        total_cost REAL,
        scene_ID INTEGER,
        session_id INTEGER,
        product_id INTEGER
    )
""",
"""
    CREATE TABLE IF NOT EXISTS discount (
        discount_id INTEGER PRIMARY KEY, 
        productName TEXT NOT NULL,
        discount REAL,
        discountDuration INTEGER NOT NULL, 
        discountStartDatetime DATETIME NOT NULL,
        product_id INTEGER
    )
""",
"""
    CREATE TABLE IF NOT EXISTS supplier (
        supplier_id INTEGER PRIMARY KEY, 
        supplierName TEXT, 
        supplierScore INTEGER NOT NULL, 
        orderDateTime DATETIME NOT NULL, 
        paymentComplete BOOLEAN, 
        orderStatus TEXT,
        product_id INTEGER
    )
""",
"""
    CREATE TABLE IF NOT EXISTS product (
        product_id INTEGER PRIMARY KEY, 
        productDescription TEXT,
        SKU VARCHAR INTEGER, 
        name TEXT NOT NULL, 
        category TEXT NOT NULL, 
        subcategory TEXT NOT NULL, 
        unitPrice REAL NOT NULL, 
        productReview REAL, 
        inventory_id INTEGER
    )
""",
"""
    CREATE TABLE IF NOT EXISTS inventory (
        inventory INTEGER PRIMARY KEY, 
        product_id INTEGER,
        quantity INTEGER NOT NULL, 
        minimumStock INTEGER, 
        maximumStock INTEGER, 
        reorderPoint INTEGER, 
        location REAL, 
        lastUpdate DATETIME
    )
"""
]
# Execute each table query 

for query in create_table_query:
    print(query)
    cursor.execute(query)


# pump data into databases



# credentials
# customerLocation
# contact
# creditCardPayment
# orderTable
# scenePlus
# payment
# orderDetails
# orderStatus
# session
# shoppingCart
# discount
# supplier
# product
# inventory

connection.commit()
connection.close()
