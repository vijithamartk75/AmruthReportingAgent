from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

load_dotenv()

server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
driver = os.getenv("DB_DRIVER")

# Encode special characters like @, #, $, %
encoded_password = quote_plus(password)

# connection_string = (
#     f"mssql+pyodbc://{username}:{encoded_password}@{server}:1433/{database}"
#     f"?driver={driver.replace(' ', '+')}&Encrypt=yes&TrustServerCertificate=no"
# )


connection_string = (
    f"mssql+pymssql://{username}:{encoded_password}@{server}:1433/{database}"
)

engine = create_engine(
    connection_string,
    pool_pre_ping=True,
    pool_recycle=3600
)

