import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    password = '',
    user = 'root',
    database = 'blog_db'
)