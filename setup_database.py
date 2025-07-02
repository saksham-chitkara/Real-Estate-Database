import pymysql

def setup_database():
    host = ''      # Fill your host (e.g., localhost)
    username = ''  # Fill your MySQL username
    password = ''  # Fill your MySQL password
    port = 3306
    db_name = ''   # Fill your database name (e.g., REAL_ESTATE)
    
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        conn.select_db(db_name)
        with open('schema.sql', 'r') as f:
            sql_content = f.read()
        statements = sql_content.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print(f"Error executing statement: {e}")
        print('Database setup complete.')
        conn.close()
    except Exception as e:
        print(f"Error setting up database: {e}")

if __name__ == "__main__":
    setup_database()
