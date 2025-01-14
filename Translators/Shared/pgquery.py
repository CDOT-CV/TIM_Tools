import os
import sqlalchemy
import logging

db_config = {
    # Pool size is the maximum number of permanent connections to keep.
    "pool_size": 5,
    # Temporarily exceeds the set pool_size if no connections are available.
    "max_overflow": 2,
    # Maximum number of seconds to wait when retrieving a
    # new connection from the pool. After the specified amount of time, an
    # exception will be thrown.
    "pool_timeout": 30,  # 30 seconds
    # 'pool_recycle' is the maximum number of seconds a connection can persist.
    # Connections that live longer than the specified amount of time will be
    # reestablished
    "pool_recycle": 60  # 1 minutes
}

db = None

def init_tcp_connection_engine(db_user, db_pass, db_name, db_hostname, db_port):
    """
    Initializes a TCP connection engine to a PostgreSQL database using the pg8000 driver.

    Args:
        db_user (str): The username for the database.
        db_pass (str): The password for the database.
        db_name (str): The name of the database.
        db_hostname (str): The hostname of the database server.
        db_port (int): The port number on which the database server is listening.

    Returns:
        sqlalchemy.engine.Engine: A SQLAlchemy engine instance connected to the specified database.
    """
    logging.info(f"Creating DB pool")
    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 5432
            database=db_name  # e.g. "my-database-name"
        ),
        **db_config
    )
    #pool.dialect.description_encoding = None
    logging.info("DB pool created!")
    return pool


def init_connection_engine():
    """
    Initializes a connection engine to a PostgreSQL database.

    This function reads database connection parameters from environment variables
    and connects to a database using TCP.

    Environment Variables:
        DB_USER (str): The database user.
        DB_PASS (str): The database password.
        DB_NAME (str): The database name.
        DB_HOST (str, optional): The database host and port in the format "hostname:port" for TCP connection.

    Returns:
        sqlalchemy.engine.Engine: A SQLAlchemy engine instance connected to the specified database.
    """
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]
    # Extract host and port from db_host
    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])
    return init_tcp_connection_engine(db_user, db_pass, db_name, db_hostname, db_port)


def query_db(query):
    """
    Executes a given SQL query on the database and returns the result.

    Args:
        query (str): The SQL query to be executed.

    Returns:
        list: A list of rows returned by the query.

    Raises:
        Exception: If there is an issue with the database connection or query execution.
    """
    global db
    if db is None:
        db = init_connection_engine()

    logging.info("DB connection starting...")
    with db.connect() as conn:
        logging.debug("Executing query...")
        data = conn.execute(query).fetchall()
        return data