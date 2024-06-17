import uuid

def generate_uuid_key():
    """
    生成一个随机的UUID作为密钥。

    Returns:
    str: 生成的UUID字符串。
    """
    return str(uuid.uuid4())

# 使用函数
key = generate_uuid_key()
print("生成的密钥为:", key)
