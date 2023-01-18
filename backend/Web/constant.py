import os
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE') or 'web'
MYSQL_USER = os.getenv('MYSQL_USER') or 'root'
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD') or '123456'
MYSQL_HOST = os.getenv('MYSQL_HOST') or 'mysql'
MYSQL_PORT = os.getenv('MYSQL_PORT')

DEBUG = os.getenv('DEBUG') == 'true'