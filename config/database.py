"""
FarmTA - Ứng dụng quản lý trang trại và lai giống vật nuôi
Database configuration
"""

import mysql.connector
from mysql.connector import Error

class DatabaseConfig:
    """Cấu hình kết nối MySQL"""
    HOST = "localhost"
    USER = "root"
    PASSWORD = ""  # Thay đổi mật khẩu MySQL của bạn
    DATABASE = "farmta_db"

def create_connection():
    """Tạo kết nối tới MySQL"""
    try:
        connection = mysql.connector.connect(
            host=DatabaseConfig.HOST,
            user=DatabaseConfig.USER,
            password=DatabaseConfig.PASSWORD,
            database=DatabaseConfig.DATABASE
        )
        return connection
    except Error as e:
        print(f"Lỗi kết nối: {e}")
        return None

def execute_query(connection, query, params=None):
    """Thực thi query"""
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor
    except Error as e:
        print(f"Lỗi thực thi query: {e}")
        return None

def fetch_query(connection, query, params=None):
    """Lấy dữ liệu từ query"""
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Lỗi lấy dữ liệu: {e}")
        return None
