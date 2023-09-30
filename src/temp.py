from sql_scripts.sql_query import check_customer_exists
import app

customer_name = "Jack"
customer_exists = check_customer_exists(app.Transactions> customer_name)
print(customer_exists)