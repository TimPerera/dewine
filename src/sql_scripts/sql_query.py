from sqlalchemy.orm import aliased
from ..src.config import create_session

session = create_session()
def check_customer_exists(table, customer_name,session=session):
    alias = aliased(table)
    query = session.query(alias).filter(alias.customer.has(first_name = customer_name))
    result = query.count() > 0
    return result

# Example usage

# def check_email():
#     pass

