"""
Database query helpers and utilities
Provides common query patterns and helper functions
"""
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class QueryBuilder:
    """Helper class for building dynamic SQL queries"""
    
    def __init__(self, table_name):
        self.table_name = table_name
        self.select_columns = ['*']
        self.where_conditions = []
        self.where_params = []
        self.join_clauses = []
        self.order_by = []
        self.group_by = []
        self.having_conditions = []
        self.limit_value = None
        self.offset_value = None
    
    def select(self, columns):
        """Set SELECT columns"""
        if isinstance(columns, list):
            self.select_columns = columns
        else:
            self.select_columns = [columns]
        return self
    
    def where(self, condition, params=None):
        """Add WHERE condition"""
        self.where_conditions.append(condition)
        if params:
            if isinstance(params, (list, tuple)):
                self.where_params.extend(params)
            else:
                self.where_params.append(params)
        return self
    
    def join(self, join_clause):
        """Add JOIN clause"""
        self.join_clauses.append(join_clause)
        return self
    
    def order(self, column, direction='ASC'):
        """Add ORDER BY clause"""
        self.order_by.append(f"{column} {direction}")
        return self
    
    def group(self, columns):
        """Add GROUP BY clause"""
        if isinstance(columns, list):
            self.group_by.extend(columns)
        else:
            self.group_by.append(columns)
        return self
    
    def having(self, condition):
        """Add HAVING clause"""
        self.having_conditions.append(condition)
        return self
    
    def limit(self, limit):
        """Set LIMIT"""
        self.limit_value = limit
        return self
    
    def offset(self, offset):
        """Set OFFSET"""
        self.offset_value = offset
        return self
    
    def build(self):
        """Build the final query"""
        # SELECT clause
        columns = ', '.join(self.select_columns)
        query = f"SELECT {columns} FROM {self.table_name}"
        
        # JOIN clauses
        if self.join_clauses:
            query += ' ' + ' '.join(self.join_clauses)
        
        # WHERE clause
        if self.where_conditions:
            query += ' WHERE ' + ' AND '.join(self.where_conditions)
        
        # GROUP BY clause
        if self.group_by:
            query += ' GROUP BY ' + ', '.join(self.group_by)
        
        # HAVING clause
        if self.having_conditions:
            query += ' HAVING ' + ' AND '.join(self.having_conditions)
        
        # ORDER BY clause
        if self.order_by:
            query += ' ORDER BY ' + ', '.join(self.order_by)
        
        # OFFSET and FETCH (MSSQL pagination)
        if self.offset_value is not None or self.limit_value is not None:
            if not self.order_by:
                # MSSQL requires ORDER BY for OFFSET/FETCH
                query += ' ORDER BY (SELECT NULL)'
            
            if self.offset_value is not None:
                query += f' OFFSET {self.offset_value} ROWS'
            else:
                query += ' OFFSET 0 ROWS'
            
            if self.limit_value is not None:
                query += f' FETCH NEXT {self.limit_value} ROWS ONLY'
        
        return query, tuple(self.where_params)


def build_insert_query(table_name: str, data: Dict[str, Any]) -> Tuple[str, tuple]:
    """
    Build INSERT query from dictionary
    
    Args:
        table_name: Table name
        data: Dictionary of column:value pairs
    
    Returns:
        Tuple of (query, params)
    """
    columns = list(data.keys())
    placeholders = ','.join(['?' for _ in columns])
    column_names = ','.join(columns)
    
    query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    params = tuple(data.values())
    
    return query, params


def build_update_query(table_name: str, data: Dict[str, Any], where_clause: str, where_params: tuple) -> Tuple[str, tuple]:
    """
    Build UPDATE query from dictionary
    
    Args:
        table_name: Table name
        data: Dictionary of column:value pairs to update
        where_clause: WHERE condition
        where_params: WHERE parameters
    
    Returns:
        Tuple of (query, params)
    """
    set_clauses = [f"{col} = ?" for col in data.keys()]
    set_clause = ', '.join(set_clauses)
    
    query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
    params = tuple(data.values()) + where_params
    
    return query, params


def build_delete_query(table_name: str, where_clause: str, where_params: tuple) -> Tuple[str, tuple]:
    """
    Build DELETE query
    
    Args:
        table_name: Table name
        where_clause: WHERE condition
        where_params: WHERE parameters
    
    Returns:
        Tuple of (query, params)
    """
    query = f"DELETE FROM {table_name} WHERE {where_clause}"
    return query, where_params


def paginate_query(query: str, page: int = 1, page_size: int = 20) -> Tuple[str, int]:
    """
    Add pagination to query (MSSQL style)
    
    Args:
        query: Base SQL query
        page: Page number (1-indexed)
        page_size: Items per page
    
    Returns:
        Tuple of (paginated_query, offset)
    """
    offset = (page - 1) * page_size
    
    # Check if query already has ORDER BY
    if 'ORDER BY' not in query.upper():
        query += ' ORDER BY (SELECT NULL)'
    
    paginated_query = f"{query} OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY"
    
    return paginated_query, offset


def build_search_condition(search_term: str, columns: List[str]) -> Tuple[str, list]:
    """
    Build search condition for multiple columns
    
    Args:
        search_term: Search term
        columns: List of columns to search
    
    Returns:
        Tuple of (condition, params)
    """
    if not search_term or not columns:
        return "", []
    
    conditions = [f"{col} LIKE ?" for col in columns]
    condition = '(' + ' OR '.join(conditions) + ')'
    params = [f"%{search_term}%" for _ in columns]
    
    return condition, params


def build_date_range_condition(column: str, start_date: Optional[datetime], end_date: Optional[datetime]) -> Tuple[str, list]:
    """
    Build date range condition
    
    Args:
        column: Date column name
        start_date: Start date
        end_date: End date
    
    Returns:
        Tuple of (condition, params)
    """
    conditions = []
    params = []
    
    if start_date:
        conditions.append(f"{column} >= ?")
        params.append(start_date)
    
    if end_date:
        conditions.append(f"{column} <= ?")
        params.append(end_date)
    
    if conditions:
        return ' AND '.join(conditions), params
    
    return "", []


def build_in_condition(column: str, values: List[Any]) -> Tuple[str, list]:
    """
    Build IN condition
    
    Args:
        column: Column name
        values: List of values
    
    Returns:
        Tuple of (condition, params)
    """
    if not values:
        return "", []
    
    placeholders = ','.join(['?' for _ in values])
    condition = f"{column} IN ({placeholders})"
    
    return condition, values


def sanitize_order_by(column: str, allowed_columns: List[str], default: str = None) -> str:
    """
    Sanitize ORDER BY column to prevent SQL injection
    
    Args:
        column: Requested column
        allowed_columns: List of allowed columns
        default: Default column if requested is not allowed
    
    Returns:
        Safe column name
    """
    if column in allowed_columns:
        return column
    
    if default and default in allowed_columns:
        return default
    
    return allowed_columns[0] if allowed_columns else 'id'


def format_sql_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format parameters for SQL query (handle None, dates, etc.)
    
    Args:
        params: Dictionary of parameters
    
    Returns:
        Formatted parameters
    """
    formatted = {}
    
    for key, value in params.items():
        if value is None:
            formatted[key] = None
        elif isinstance(value, datetime):
            formatted[key] = value
        elif isinstance(value, bool):
            formatted[key] = 1 if value else 0
        else:
            formatted[key] = value
    
    return formatted


def row_to_dict(cursor, row) -> Dict[str, Any]:
    """
    Convert database row to dictionary
    
    Args:
        cursor: Database cursor
        row: Database row
    
    Returns:
        Dictionary representation
    """
    if not row:
        return None
    
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))


def rows_to_dict_list(cursor, rows) -> List[Dict[str, Any]]:
    """
    Convert database rows to list of dictionaries
    
    Args:
        cursor: Database cursor
        rows: Database rows
    
    Returns:
        List of dictionaries
    """
    if not rows:
        return []
    
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in rows]
