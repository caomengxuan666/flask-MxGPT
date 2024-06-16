import hashlib
import pymysql
from dbutils.pooled_db import PooledDB
import uuid
from psycopg2 import IntegrityError
from sqlCheck import check_mysql_keywords,check_special_characters

# 配置数据库连接池
POOL = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=3,
    blocking=True,
    setsession=[],
    ping=0,
    host='120.26.73.234',
    port=3306,
    user='root',
    password='mx123321',
    charset='utf8',
    db='mxgpt'
)


def get_db_connection():
    return POOL.connection()

def check_unique_username_and_id(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = %s OR id = %s", (username, username))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is None

def register_user(username, password):
    if not check_unique_username_and_id(username):
        raise ValueError("Username or ID already exists.")

    # V1.5.0 新增：检查用户名是否包含MySQL关键字
    if not check_mysql_keywords(username):
        raise ValueError("Username cannot contain MySQL keywords")

    if not check_special_characters(username):
        raise ValueError("Username cannot contain special characters.")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user_id = str(uuid.uuid4())

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (id, username, password) VALUES (%s, %s, %s)",
                       (user_id, username, hashed_password))
        conn.commit()
    except IntegrityError:
        # 如果插入时仍发生唯一性冲突（理论上前面的检查应避免这种情况，但保险起见还是捕获异常）
        raise ValueError("Username or ID already exists during insertion.")
    finally:
        cursor.close()
        conn.close()

    return user_id

def validate_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return user
