import sqlite3


class DatabaseConnection:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def createTable(self):
        conn = sqlite3.connect(self.database_file)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE contacts (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                type VARCHAR(20),
                phone VARCHAR(20),
                email VARCHAR(100)
            )
        ''')
        conn.commit()
        conn.close()


    def connect(self):
        conn = sqlite3.connect(self.database_file)
        return conn


# DatabaseConnection().createTable()