import hashlib
import pymysql
from dbutils.pooled_db import PooledDB
import uuid

# 配置数据库连接池
POOL = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=3,
    blocking=True,
    setsession=[],
    ping=0,
    host='127.0.0.1',
    port=3306,
    user='root',
    password='mx123321',
    charset='utf8',
    db='mxgpt'
)


def get_db_connection():
    return POOL.connection()


def register_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user_id = str(uuid.uuid4())

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (id, username, password) VALUES (%s, %s, %s)",
                   (user_id, username, hashed_password))
    conn.commit()
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
