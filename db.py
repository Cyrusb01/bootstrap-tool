import psycopg2
from sqlalchemy import create_engine



db_password = "Frog2001"

engine = create_engine('postgresql://postgres:{}@localhost/stock_data_database'.format(db_password))

