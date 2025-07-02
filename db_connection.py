import pymysql
import pymysql.cursors
from colorama import Fore, Style, init
init(autoreset=True)
SUCCESS = Fore.GREEN + Style.BRIGHT

class DBconnection:
    # DB connection info
    username = ""  # Fill your MySQL username
    password = ""  # Fill your MySQL password
    db_name = ""   # Fill your database name (e.g., REAL_ESTATE)
    host = ""      # Fill your host (e.g., localhost)
    port = 3306

    conn = None
    cursor = None
    try_to_connect = 0

    def __init__(self, host=None, username=None, password=None, db_name=None, port=None):
        self.username = username or self.username
        self.password = password or self.password
        self.db_name = db_name or self.db_name
        self.host = host or self.host
        self.port = port or self.port
        self.connect()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print('Database connection closed.')

    def execute_query(self, query, params=None, fetch=False):
        # Accept (query, params) tuple or just query string
        if isinstance(query, tuple):
            query, params = query
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        if fetch:
            return self.cursor.fetchall()
        else:
            self.conn.commit()
            return True

    def connect(self):
        self.try_to_connect += 1
        print()
        print(SUCCESS + f'({self.try_to_connect}) Trying to connect to {self.db_name}...')
        try:
            self.conn = pymysql.connect(host=self.host,
                                        port=self.port,
                                        user=self.username,
                                        password=self.password,
                                        database=self.db_name,
                                        cursorclass=pymysql.cursors.DictCursor)
            if self.conn.open:
                print(SUCCESS + "Connected")
                print()
            else:
                raise Exception("Failed to connect")
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("Error occurred")
            print(e)
        finally:
            if self.try_to_connect < 5 and self.conn is None:
                print('Trying to reconnect...')
                self.connect()
