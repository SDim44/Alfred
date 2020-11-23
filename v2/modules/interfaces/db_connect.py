#       Homestead Database Connector
#
#       Autor:              Stefan Dimnik
#       Date:               28.09.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Homestead
#       ------------------------------------------------------------
#       
#       V0.1
#       Database connection
#       ------------------------------------------------------------

import pymysql.cursors

connection = pymysql.connect(host='localhost',
user='python_logger',
password='dij)4k!diD3J',
db='homestead',
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor)

def insert(tb,publisher,value):
    try:
        with connection.cursor() as cursor:
            sql = 'INSERT INTO ' , tb , ' (`publisher`, `value`) VALUES (%s, %s)'
            cursor.execute(sql, (publisher,value))
        connection.commit()

    finally:
        connection.close()
