import plotly.express as px
import pandas as pd
from database import Database
import os.path
import sqlite3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database_new.db")
with sqlite3.connect(db_path) as conn:

    sweetness_hist = Database.execute_query(conn, "SELECT sweet, COUNT(*) AS count_sweet FROM characteristics_table GROUP BY sweet;")
    acidity_hist = Database.execute_query(conn, "SELECT acidity, COUNT(*) AS count_acidity FROM characteristics_table GROUP BY acidity;")
    body_hist = Database.execute_query(conn, "SELECT body, COUNT(*) AS count_body FROM characteristics_table GROUP BY body;")
    tannin_hist = Database.execute_query(conn, "SELECT tannin, COUNT(*) AS count_tannin FROM characteristics_table GROUP BY tannin;")
    
    cursors = [sweetness_hist, acidity_hist, body_hist, tannin_hist]
    taste_hist_df = [Database.cursor_to_df(cursor) for cursor in cursors]    
    taste_hist_df = pd.concat(taste_hist_df, axis=1)
    
    
    # 2.
    # SELECT abv, AVG(price) AS avg_price FROM characteristics_table INNER JOIN sales_table ON characteristics_table.id = sales_table.characteristics_id GROUP BY abv;

    abv_price = Database.execute_query(conn, "SELECT abv, AVG(price) AS avg_price FROM characteristics_table INNER JOIN sales_table ON characteristics_table.id = sales_table.characteristics_id GROUP BY abv;")
    abv_price_df = Database.cursor_to_df(abv_price)
    
    #3.
    # SELECT year, AVG(price) AS avg_price FROM sales_table GROUP BY year;
    
    by_year_price = Database.execute_query(conn, "SELECT year, AVG(price) AS avg_price FROM sales_table GROUP BY year;")
    by_year_price_df = Database.cursor_to_df(by_year_price)
    

    # 4.
    # SELECT v.variety, c.sweet, c.acidity, c.body, c.tannin FROM varieties_table v 
    # INNER JOIN sales_table s ON v.id = s.variety_id 
    # INNER JOIN characteristics_table c ON s.characteristics_id = c.id;
    
    # fig_by_variety = Database.execute_query(conn, "SELECT v.variety, c.sweet, c.acidity, c.body, c.tannin FROM varieties_table v INNER JOIN sales_table s ON v.id = s.variety_id INNER JOIN characteristics_table c ON s.characteristics_id = c.id;")
    # fig_by_variety_df = Database.cursor_to_df(fig_by_variety)
    

    # 5.
    # SELECT nation, COUNT(*) AS production_count FROM locations_table GROUP BY nation;
    
    production_by_nation = Database.execute_query(conn, "SELECT nation, COUNT(*) AS production_count FROM locations_table GROUP BY nation;")
    production_by_nation_df = Database.cursor_to_df(production_by_nation)

    # 6.
    # SELECT p.name, COUNT(*) AS total_sales FROM products_table p 
    # INNER JOIN sales_table s ON p.id = s.product_id 
    # GROUP BY p.name ORDER BY total_sales DESC;
    
    most_sold_products = Database.execute_query(conn, "SELECT p.name, COUNT(*) AS total_sales FROM products_table p INNER JOIN sales_table s ON p.id = s.product_id GROUP BY p.name ORDER BY total_sales DESC;")
    most_sold_products_df = Database.cursor_to_df(most_sold_products)

    # 7.
    # SELECT p.type, COUNT(*) AS count_type FROM products_table p GROUP BY p.type;
    
    wine_type_count = Database.execute_query(conn, "SELECT p.type, COUNT(*) AS count_type FROM products_table p GROUP BY p.type;")
    wine_type_count_df = Database.cursor_to_df(wine_type_count)

    
    
    