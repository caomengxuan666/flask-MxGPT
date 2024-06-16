"""
这个模块是为了防止SQL注入设计的，在注册时对注册的信息做出限定
这里分别处理MySQL关键字和特殊字符的检查，以增强用户名的安全性
"""

import re

# 注册用户时禁用的MySQL关键字列表
mysql_keywords = [
    "SELECT", "UPDATE", "DELETE", "INSERT", "ALTER",
    "CREATE", "DROP", "TRUNCATE", "GRANT", "REVOKE"
]

# 构建MySQL关键字的正则表达式模式
mysql_keyword_pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, mysql_keywords)) + r')\b', re.IGNORECASE)


def check_mysql_keywords(username):
    """检查用户名是否包含MySQL关键字"""
    return mysql_keyword_pattern.search(username) is None


# 注册用户时禁用的特殊字符列表
special_characters = [
    "\\", "|", "&", "^", "=", "<", ">", "!", "~",
    "(", ")", "{", "}", "[", "]", ";", ":", ",",
    "'", '"', "`", "@", "#", "$", "%", "*", "+",
    "-", "?", "/", ".", " "
]

# 构建特殊字符的正则表达式模式
special_char_pattern = re.compile(r'(?:' + '|'.join(map(re.escape, special_characters)) + ')')


def check_special_characters(username):
    """检查用户名是否包含特殊字符"""
    return special_char_pattern.search(username) is None
