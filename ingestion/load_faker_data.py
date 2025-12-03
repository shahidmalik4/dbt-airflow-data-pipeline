import psycopg2
from faker import Faker
import random

fake = Faker()

# -----------------------------
# Connect to Postgres
# -----------------------------
conn = psycopg2.connect(
    f"dbname={os.getenv('POSTGRES_DB')} "
    f"user={os.getenv('POSTGRES_USER')} "
    f"password={os.getenv('POSTGRES_PASSWORD')} "
    f"host=localhost "
    f"port={os.getenv('POSTGRES_PORT')}"
)

cur = conn.cursor()

# -----------------------------
# Drop tables if they exist
# -----------------------------
cur.execute("""
DROP TABLE IF EXISTS raw.order_details;
DROP TABLE IF EXISTS raw.orders;
DROP TABLE IF EXISTS raw.products;
DROP TABLE IF EXISTS raw.customers;
""")

# -----------------------------
# Create tables
# -----------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS raw.customers (
    customer_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    address TEXT,
    signup_date DATE
);

CREATE TABLE IF NOT EXISTS raw.products (
    product_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    price NUMERIC(10,2),
    inventory INT
);

CREATE TABLE IF NOT EXISTS raw.orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES raw.customers(customer_id),
    order_date DATE,
    total_amount NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS raw.order_details (
    order_detail_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES raw.orders(order_id),
    product_id INT REFERENCES raw.products(product_id),
    quantity INT,
    price NUMERIC(10,2)
);
""")
conn.commit()
print("Tables created successfully in raw schema!")

# -----------------------------
# Parameters
# -----------------------------
NUM_CUSTOMERS = 500      # adjust as needed
NUM_PRODUCTS = 4300       # adjust as needed
BATCH_SIZE = 500

# -----------------------------
# Insert Customers
# -----------------------------
customer_ids = []
customer_batch = []

for _ in range(NUM_CUSTOMERS):
    customer_batch.append((
        fake.name(),
        fake.unique.email(),
        fake.address().replace("\n", ", "),
        fake.date_between(start_date='-2y', end_date='today')
    ))

    if len(customer_batch) >= BATCH_SIZE:
        values_str = ",".join(cur.mogrify("(%s, %s, %s, %s)", row).decode('utf-8') for row in customer_batch)
        cur.execute(f"INSERT INTO raw.customers (name, email, address, signup_date) VALUES {values_str} RETURNING customer_id;")
        customer_ids.extend([row[0] for row in cur.fetchall()])
        conn.commit()
        customer_batch = []

if customer_batch:
    values_str = ",".join(cur.mogrify("(%s, %s, %s, %s)", row).decode('utf-8') for row in customer_batch)
    cur.execute(f"INSERT INTO raw.customers (name, email, address, signup_date) VALUES {values_str} RETURNING customer_id;")
    customer_ids.extend([row[0] for row in cur.fetchall()])
    conn.commit()

print(f"{len(customer_ids)} customers inserted.")

# -----------------------------
# Insert Products
# -----------------------------
product_ids = []
product_batch = []

for _ in range(NUM_PRODUCTS):
    product_batch.append((
        fake.word().capitalize() + " " + fake.word().capitalize(),
        fake.word().capitalize(),
        round(random.uniform(5, 500), 2),
        random.randint(10, 1000)
    ))

    if len(product_batch) >= BATCH_SIZE:
        values_str = ",".join(cur.mogrify("(%s, %s, %s, %s)", row).decode('utf-8') for row in product_batch)
        cur.execute(f"INSERT INTO raw.products (name, category, price, inventory) VALUES {values_str} RETURNING product_id;")
        product_ids.extend([row[0] for row in cur.fetchall()])
        conn.commit()
        product_batch = []

if product_batch:
    values_str = ",".join(cur.mogrify("(%s, %s, %s, %s)", row).decode('utf-8') for row in product_batch)
    cur.execute(f"INSERT INTO raw.products (name, category, price, inventory) VALUES {values_str} RETURNING product_id;")
    product_ids.extend([row[0] for row in cur.fetchall()])
    conn.commit()

print(f"{len(product_ids)} products inserted.")

# -----------------------------
# Insert Orders & Order Details
# -----------------------------
total_orders = 0
total_order_details = 0
orders_batch = []
order_details_batch = []

for customer_id in customer_ids:
    num_orders = random.randint(1, 400)  # 1-400 orders per customer
    for _ in range(num_orders):
        order_date = fake.date_between(start_date='-1y', end_date='today')
        orders_batch.append((customer_id, order_date, 0))
        total_orders += 1

        # Batch insert orders
        if len(orders_batch) >= BATCH_SIZE:
            values_str = ",".join(cur.mogrify("(%s, %s, %s)", row).decode('utf-8') for row in orders_batch)
            cur.execute(f"INSERT INTO raw.orders (customer_id, order_date, total_amount) VALUES {values_str} RETURNING order_id;")
            order_ids = [row[0] for row in cur.fetchall()]

            # Generate order_details
            for order_id in order_ids:
                num_items = random.randint(1, 120)  # 1-120 items per order
                total_amount = 0
                for _ in range(num_items):
                    product_id = random.choice(product_ids)
                    cur.execute("SELECT price FROM raw.products WHERE product_id = %s", (product_id,))
                    price = cur.fetchone()[0]
                    quantity = random.randint(1, 5)
                    total_amount += price * quantity
                    order_details_batch.append((order_id, product_id, quantity, price))
                    total_order_details += 1
                cur.execute("UPDATE raw.orders SET total_amount = %s WHERE order_id = %s", (total_amount, order_id))

            # Batch insert order_details
            while len(order_details_batch) >= BATCH_SIZE:
                batch = order_details_batch[:BATCH_SIZE]
                order_details_batch = order_details_batch[BATCH_SIZE:]
                values_str = ",".join(cur.mogrify("(%s, %s, %s, %s)", row).decode('utf-8') for row in batch)
                cur.execute(f"INSERT INTO raw.order_details (order_id, product_id, quantity, price) VALUES {values_str}")
                conn.commit()

            orders_batch = []

# Insert remaining orders
if orders_batch:
    values_str = ",".join(cur.mogrify("(%s, %s, %s)", row).decode('utf-8') for row in orders_batch)
    cur.execute(f"INSERT INTO raw.orders (customer_id, order_date, total_amount) VALUES {values_str} RETURNING order_id;")
    order_ids = [row[0] for row in cur.fetchall()]

    for order_id in order_ids:
        num_items = random.randint(1, 120)
        total_amount = 0
        for _ in range(num_items):
            product_id = random.choice(product_ids)
            cur.execute("SELECT price FROM raw.products WHERE product_id = %s", (product_id,))
            price = cur.fetchone()[0]
            quantity = random.randint(1, 5)
            total_amount += price * quantity
            order_details_batch.append((order_id, product_id, quantity, price))
            total_order_details += 1
        cur.execute("UPDATE raw.orders SET total_amount = %s WHERE order_id = %s", (total_amount, order_id))

# Insert remaining order_details
if order_details_batch:
    values_str = ",".join(cur.mogrify("(%s, %s, %s, %s)", row).decode('utf-8') for row in order_details_batch)
    cur.execute(f"INSERT INTO raw.order_details (order_id, product_id, quantity, price) VALUES {values_str}")
    conn.commit()

# -----------------------------
# Print Summary
# -----------------------------
cur.execute("SELECT COUNT(*) FROM raw.customers")
num_customers = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM raw.products")
num_products = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM raw.orders")
num_orders = cur.fetchone()[0]

print("\n===== DATA INSERTION SUMMARY =====")
print(f"Customers table: {num_customers} rows")
print(f"Products table: {num_products} rows")
print(f"Orders table: {num_orders} rows")
print(f"Order Details table: {total_order_details} rows")
print("===================================")

cur.close()
conn.close()
