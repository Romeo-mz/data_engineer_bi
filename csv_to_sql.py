import pandas as pd
import sqlite3

# Read CSV into a DataFrame
df = pd.read_csv('clean_data/cleaned_wine_info.csv')

# Establish connection to SQLite database
conn = sqlite3.connect('La_base.db')
cur = conn.cursor()

# Define SQL CREATE TABLE statements for the tables de dimensions
create_products_table_sql = """
CREATE TABLE IF NOT EXISTS products_table (
    id INTEGER PRIMARY KEY,
    name TEXT,
    producer TEXT,
    type TEXT
);
"""

create_locations_table_sql = """
CREATE TABLE IF NOT EXISTS locations_table (
    id INTEGER PRIMARY KEY,
    nation TEXT,
    local1 TEXT
);
"""

create_varieties_table_sql = """
CREATE TABLE IF NOT EXISTS varieties_table (
    id INTEGER PRIMARY KEY,
    variety TEXT
);
"""

create_characteristics_table_sql = """
CREATE TABLE IF NOT EXISTS characteristics_table (
    id INTEGER PRIMARY KEY,
    type TEXT,
    abv TEXT,
    degree TEXT,
    sweet TEXT,
    acidity TEXT,
    body TEXT,
    tannin TEXT
);
"""

# Define SQL CREATE TABLE statement for the table de faits
create_sales_table_sql = """
CREATE TABLE IF NOT EXISTS sales_table (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    location_id INTEGER,
    variety_id INTEGER,
    characteristics_id INTEGER,
    price INTEGER,
    FOREIGN KEY (product_id) REFERENCES products_table (id),
    FOREIGN KEY (location_id) REFERENCES locations_table (id),
    FOREIGN KEY (variety_id) REFERENCES varieties_table (id),
    FOREIGN KEY (characteristics_id) REFERENCES characteristics_table (id)
);
"""

# Create the tables de dimensions
cur.execute(create_products_table_sql)
cur.execute(create_locations_table_sql)
cur.execute(create_varieties_table_sql)
cur.execute(create_characteristics_table_sql)

# Create the table de faits
cur.execute(create_sales_table_sql)

# Insert data into the tables de dimensions
for index, row in df.iterrows():
    # Insert data into products_table
    product_insert_sql = "INSERT INTO products_table (name, producer, type) VALUES (?, ?, ?)"
    cur.execute(product_insert_sql, (row['name'], row['producer'], row['type']))

    # Insert data into locations_table
    location_insert_sql = "INSERT INTO locations_table (nation, local1) VALUES (?, ?)"
    cur.execute(location_insert_sql, (row['nation'], row['local1']))

    # Insert data into varieties_table
    variety_insert_sql = "INSERT INTO varieties_table (variety) VALUES (?)"
    cur.execute(variety_insert_sql, (row['varieties1'],))

    # Insert data into characteristics_table
    characteristics_insert_sql = "INSERT INTO characteristics_table (type, abv, degree, sweet, acidity, body, tannin) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cur.execute(characteristics_insert_sql, (row['type'], row['abv'], row['degree'], row['sweet'], row['acidity'], row['body'], row['tannin']))

# Commit changes to dimensions tables
conn.commit()

# Insert data into the table de faits
for index, row in df.iterrows():
    # Get the foreign keys for each dimension from their respective tables
    product_id_sql = "SELECT id FROM products_table WHERE name=? AND producer=? AND type=?"
    cur.execute(product_id_sql, (row['name'], row['producer'], row['type']))
    product_id = cur.fetchone()[0]

    location_id_sql = "SELECT id FROM locations_table WHERE nation=? AND local1=?"
    cur.execute(location_id_sql, (row['nation'], row['local1']))
    location_id = cur.fetchone()[0]

    variety_id_sql = "SELECT id FROM varieties_table WHERE variety=?"
    cur.execute(variety_id_sql, (row['varieties1'],))
    variety_id = cur.fetchone()[0]

    characteristics_id_sql = "SELECT id FROM characteristics_table WHERE type=? AND abv=? AND degree=? AND sweet=? AND acidity=? AND body=? AND tannin=?"
    cur.execute(characteristics_id_sql, (row['type'], row['abv'], row['degree'], row['sweet'], row['acidity'], row['body'], row['tannin']))
    characteristics_id = cur.fetchone()[0]

    # Insert data into sales_table
    sales_insert_sql = "INSERT INTO sales_table (product_id, location_id, variety_id, characteristics_id, price) VALUES (?, ?, ?, ?, ?)"
    cur.execute(sales_insert_sql, (product_id, location_id, variety_id, characteristics_id, row['price']))

# Commit changes to the sales table
conn.commit()

# Close connection
conn.close()
