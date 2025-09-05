import mysql.connector

def query_db(query, config, params=None):
    db_conf = config["db"]
    conn = mysql.connector.connect(
        host=db_conf["host"],
        user=db_conf["user"],
        password=db_conf["password"],
        database=db_conf["database"]
    )
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    conn.close()
    return result
