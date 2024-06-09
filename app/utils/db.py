import mysql.connector
from mysql.connector import errorcode
import logging
from functools import wraps

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    pass


class AccessDeniedError(DatabaseError):
    pass


class DatabaseDoesNotExistError(DatabaseError):
    pass


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise AccessDeniedError("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise DatabaseDoesNotExistError("Database does not exist")
        else:
            raise DatabaseError(err)


def with_db_connection(func):
    def wrapper(*args, **kwargs):
        connection = get_db_connection()
        try:
            result = func(connection, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error during DB operation: {e}")
            raise
        finally:
            connection.close()
        return result
    return wrapper


def with_db_connection_and_cursor(func):
    @with_db_connection
    def wrapper(connection, *args, **kwargs):
        cursor_dictionary = kwargs.pop('dictionary', False)
        cursor = connection.cursor(dictionary=cursor_dictionary)
        try:
            result = func(connection, cursor, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error during DB cursor operation: {e}")
            raise
        finally:
            cursor.close()
        return result
    return wrapper


@with_db_connection_and_cursor
def execute_and_fetchone(connection, cursor, query, params, **kwargs):
    cursor.execute(query, params, **kwargs)
    return cursor.fetchone()


@with_db_connection_and_cursor
def execute_and_fetchall(connection, cursor, query, params, **kwargs):
    cursor.execute(query, params, **kwargs)
    return cursor.fetchall()


@with_db_connection_and_cursor
def execute_and_commit(connection, cursor, query, params, **kwargs):
    cursor.execute(query, params, **kwargs)
    connection.commit()


def transactional(func):
  @wraps(func)
  @with_db_connection
  def wrapper(connection, cursor, *args, **kwargs):
    try:
      result = func(cursor, *args, **kwargs)
      connection.commit()  # Commit within wrapper
      return result
    except Exception as e:
      connection.rollback()
      logger.error(f"Error during {func.__name__}: {e}")
      raise
  return wrapper