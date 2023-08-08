import sqlite3

# create table
connection = sqlite3.connect('voila.db')

cursor = connection.cursor()

create_table_query = ["""
    CREATE TABLE IF NOT EXISTS customer (
        customer_uuid INTEGER PRIMARY KEY,
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL,
        sceneID
        )

""",
"""
    CREATE TABLE IF NOT EXISTS credentials (
        credentials_id INTEGER PRIMARY KEY,
        customer_uuid INTEGER,
        password_hash TEXT,
        password_salt TEXT,
        FOREIGN KEY(customer_uuid) REFERENCES customer(customer_uuid)
    )
""",
"""
    CREATE TABLE IF NOT EXISTS customerLocation (
        address_id INTEGER PRIMARY KEY, 
        customer_uuid INTEGER,
        unitNumber INTEGER, 
        building_name TEXT,
        postal_code VARCHAR,
        FOREIGN KEY(customer_uuid) REFERENCES customer(customer_uuid)
    )
""",
"""
    CREATE TABLE IF NOT EXISTS contact (
        contact_id INTEGER PRIMARY KEY,
        customer_uuid INTEGER,
        email TEXT NOT NULL UNIQUE,
        phone INTEGER NOT NULL UNIQUE,
        address_id INTEGER,
        FOREIGN KEY(address_id) REFERENCES customerLocation(address_id),
        FOREIGN KEY(customer_uuid) REFERENCES customer(customer_uuid)
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
        customer_uuid INTEGER,
        orderDetails_id INTEGER, 
        shoppingCart_id INTEGER,
        session_id INTEGER,
        orderStatus_id INTEGER,
        payment_id INTEGER,
        FOREIGN KEY(customer_uuid) REFERENCES customer(customer_uuid),
        FOREIGN KEY(orderDetails_id) REFERENCES orderDetails(orderDetails_id),
        FOREIGN KEY(shoppingCart_id) REFERENCES shoppingCart(shoppingCart_id),
        FOREIGN KEY(session_id) REFERENCES session(session_id),
        FOREIGN KEY(orderStatus_id) REFERENCES orderStatus(orderStatus_id),
        FOREIGN KEY(payment_id) REFERENCES payment(payment_id)
    )
""",
"""
    CREATE TABLE IF NOT EXISTS scenePlus (
        scene_ID INTEGER PRIMARY KEY,
        customer_uuid INTEGER,
        points REAL,
        FOREIGN KEY(customer_uuid) REFERENCES customer(customer_uuid)
    )
""",
"""
    CREATE TABLE IF NOT EXISTS payment (
        payment_id INTEGER PRIMARY KEY,
        datetime DATETIME NOT NULL,
        amount FLOAT NOT NULL,
        card_id INTEGER,
        order_id INTEGER,
        FOREIGN KEY(card_id) REFERENCES card(card_id),
        FOREIGN KEY (order_id) REFERENCES orderTable(order_id)

    )
""",
"""
    CREATE TABLE IF NOT EXISTS orderDetails(
        orderDetails_id INTEGER PRIMARY KEY, 
        order_id INTEGER,
        product_id INTEGER,
        discount REAL,
        FOREIGN KEY(order_id) REFERENCES orderTable(order_id),
        FOREIGN KEY(product_id) REFERENCES product(product_id),
        FOREIGN KEY(discount) REFERENCES discount(discount)
    )
""",
"""
    CREATE TABLE IF NOT EXISTS orderStatus (
        orderStatus_id INTEGER PRIMARY KEY, 
        orderStatus TEXT NOT NULL, 
        statusDate DATE NOT NULL, 
        gpsCoord REAL,
        order_id INTEGER,
        FOREIGN KEY(order_id) REFERENCES orderTable(order_id)
    )
""",
"""
    CREATE TABLE IF NOT EXISTS session (
        session_id INTEGER PRIMARY KEY,
        created_at DATETIME,
        ended_at DATETIME,
        sessionTime TIME,
        customer_uuid INTEGER,
        FOREIGN KEY(customer_uuid) REFERENCES customer(customer_uuid)
    )
""",
"""
    CREATE TABLE IF NOT EXISTS shoppingCart (
        shoppingCart_id INTEGER PRIMARY KEY,
        quantity INTEGER NOT NULL,
        total_cost REAL,
        customer_uuid INTEGER,
        session_id INTEGER,
        product_id INTEGER,
        FOREIGN KEY(customer_uuid) REFERENCES customer(customer_uuid),
        FOREIGN KEY(session_id) REFERENCES session(session_id),
        FOREIGN KEY(product_id) REFERENCES product(product_id)
    )
""",
"""
    CREATE TABLE IF NOT EXISTS discount (
        discount_id INTEGER PRIMARY KEY, 
        productName TEXT NOT NULL,
        discount REAL,
        discountDuration INTEGER NOT NULL, 
        discountStartDatetime DATETIME NOT NULL,
        product_id INTEGER,
        FOREIGN KEY(product_id) REFERENCES product(product_id)
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
        product_id INTEGER,
        FOREIGN KEY(product_id) REFERENCES product(product_id)
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
        inventory_id INTEGER,
        FOREIGN KEY(inventory_id) REFERENCES inventory(inventory_id)
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
        lastUpdate DATETIME,
        FOREIGN KEY(product_id) REFERENCES product(product_id)
    )
"""
]
# Execute each table query 

for query in create_table_query:
    print(query)
    cursor.execute(query)


# pump data into databases

# customer
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
