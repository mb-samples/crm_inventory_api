"""
Database connection module with connection pooling
Handles MSSQL connections using pyodbc
"""
import pyodbc
import logging
from contextlib import contextmanager
from threading import Lock
from queue import Queue, Empty
from config.config import get_config

logger = logging.getLogger(__name__)

class DatabaseConnectionPool:
    """Connection pool manager for MSSQL database"""
    
    def __init__(self, config):
        self.config = config
        self.pool_size = config.DB_POOL_SIZE
        self.max_overflow = config.DB_MAX_OVERFLOW
        self.timeout = config.DB_POOL_TIMEOUT
        self.connection_string = config.DATABASE_URI
        
        self._pool = Queue(maxsize=self.pool_size + self.max_overflow)
        self._lock = Lock()
        self._current_size = 0
        
        # Initialize pool with minimum connections
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize the connection pool with base connections"""
        try:
            for _ in range(self.pool_size):
                conn = self._create_connection()
                self._pool.put(conn)
                self._current_size += 1
            logger.info(f"Connection pool initialized with {self.pool_size} connections")
        except Exception as e:
            logger.error(f"Failed to initialize connection pool: {str(e)}")
            raise
    
    def _create_connection(self):
        """Create a new database connection"""
        try:
            conn = pyodbc.connect(self.connection_string, timeout=self.timeout)
            conn.autocommit = False
            logger.debug("New database connection created")
            return conn
        except pyodbc.Error as e:
            logger.error(f"Failed to create database connection: {str(e)}")
            raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        try:
            # Try to get connection from pool with timeout
            conn = self._pool.get(timeout=self.timeout)
            
            # Test if connection is still valid
            try:
                conn.cursor().execute("SELECT 1")
                return conn
            except:
                # Connection is dead, create a new one
                logger.warning("Dead connection detected, creating new one")
                conn.close()
                return self._create_connection()
                
        except Empty:
            # Pool is empty, try to create overflow connection
            with self._lock:
                if self._current_size < (self.pool_size + self.max_overflow):
                    conn = self._create_connection()
                    self._current_size += 1
                    logger.info(f"Created overflow connection. Current size: {self._current_size}")
                    return conn
                else:
                    raise Exception("Connection pool exhausted and max overflow reached")
    
    def return_connection(self, conn):
        """Return a connection to the pool"""
        try:
            if conn and not conn.closed:
                # Rollback any uncommitted transactions
                try:
                    conn.rollback()
                except:
                    pass
                
                # Return to pool if not full
                if self._pool.qsize() < (self.pool_size + self.max_overflow):
                    self._pool.put(conn)
                else:
                    conn.close()
                    with self._lock:
                        self._current_size -= 1
        except Exception as e:
            logger.error(f"Error returning connection to pool: {str(e)}")
    
    def close_all(self):
        """Close all connections in the pool"""
        while not self._pool.empty():
            try:
                conn = self._pool.get_nowait()
                conn.close()
            except Empty:
                break
            except Exception as e:
                logger.error(f"Error closing connection: {str(e)}")
        
        self._current_size = 0
        logger.info("All connections closed")


# Global connection pool instance
_connection_pool = None
_pool_lock = Lock()


def initialize_pool(config=None):
    """Initialize the global connection pool"""
    global _connection_pool
    
    if _connection_pool is None:
        with _pool_lock:
            if _connection_pool is None:
                if config is None:
                    config = get_config()
                _connection_pool = DatabaseConnectionPool(config)
                logger.info("Global connection pool initialized")
    
    return _connection_pool


def get_pool():
    """Get the global connection pool instance"""
    global _connection_pool
    
    if _connection_pool is None:
        initialize_pool()
    
    return _connection_pool


@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    pool = get_pool()
    conn = None
    
    try:
        conn = pool.get_connection()
        yield conn
    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except:
                pass
        logger.error(f"Database connection error: {str(e)}")
        raise
    finally:
        if conn:
            pool.return_connection(conn)


@contextmanager
def get_db_cursor(commit=False):
    """Context manager for database cursor with optional auto-commit"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            if commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database cursor error: {str(e)}")
            raise
        finally:
            cursor.close()


def execute_query(query, params=None, fetch_one=False, fetch_all=True, commit=False):
    """
    Execute a SQL query and return results
    
    Args:
        query: SQL query string
        params: Query parameters (tuple or dict)
        fetch_one: Return single row
        fetch_all: Return all rows
        commit: Commit transaction after execution
    
    Returns:
        Query results or None
    """
    with get_db_cursor(commit=commit) as cursor:
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch_one:
                row = cursor.fetchone()
                return dict(zip([column[0] for column in cursor.description], row)) if row else None
            elif fetch_all:
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                return cursor.rowcount
                
        except pyodbc.Error as e:
            logger.error(f"Query execution error: {str(e)}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise


def execute_many(query, params_list, commit=True):
    """
    Execute a query multiple times with different parameters
    
    Args:
        query: SQL query string
        params_list: List of parameter tuples
        commit: Commit transaction after execution
    
    Returns:
        Number of affected rows
    """
    with get_db_cursor(commit=commit) as cursor:
        try:
            cursor.executemany(query, params_list)
            return cursor.rowcount
        except pyodbc.Error as e:
            logger.error(f"Batch execution error: {str(e)}")
            raise


def execute_transaction(queries_with_params):
    """
    Execute multiple queries in a single transaction
    
    Args:
        queries_with_params: List of tuples (query, params)
    
    Returns:
        True if successful
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            for query, params in queries_with_params:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
            
            conn.commit()
            return True
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction error: {str(e)}")
            raise
        finally:
            cursor.close()


def call_stored_procedure(proc_name, params=None):
    """
    Call a stored procedure
    
    Args:
        proc_name: Stored procedure name
        params: Procedure parameters
    
    Returns:
        Result set from procedure
    """
    with get_db_cursor() as cursor:
        try:
            if params:
                placeholders = ','.join(['?' for _ in params])
                query = f"EXEC {proc_name} {placeholders}"
                cursor.execute(query, params)
            else:
                cursor.execute(f"EXEC {proc_name}")
            
            # Fetch results if any
            if cursor.description:
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                return None
                
        except pyodbc.Error as e:
            logger.error(f"Stored procedure error: {str(e)}")
            raise


def test_connection():
    """Test database connection"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT @@VERSION as version, GETDATE() as current_time")
            result = cursor.fetchone()
            logger.info(f"Database connection successful: {result[0]}")
            return True
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return False


# Alias for backward compatibility
get_connection = get_db_connection


def close_all():
    """Close all connections in the pool"""
    global _connection_pool
    if _connection_pool:
        _connection_pool.close_all()
