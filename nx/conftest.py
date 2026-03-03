import pymysql
import pytest
import allure
@pytest.fixture(scope='function')
def parse_db_config():
    import re
    db_str = "root/root@10.10.105.152:33306/nx_app"
    pattern = r'^([^/]+)/([^@]+)@([^:]+):(\d+)/([^/]+)$'
    match = re.match(pattern, db_str)
    if not match:
        raise ValueError("Invalid database connection string format")
    user, password, host, port, db = match.groups()
    return {
        'host': host,
        'user': user,
        'password': password,
        'db': db,
        'port': int(port),
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }