# %%
import sqlite3
# from pandas import DataFrame
import pandas as pd


class Database:

    """
    sqlite3 database class for handling data operations
    inspired by:
    https://gist.github.com/goldsborough/c973d934f620e16678bf
    """

    def __init__(self, name=None):
        """ Instantiate database class. Open a database if a name is
        provided. Otherwise don't open a database. A database can
        be opened manually by calling the open() method.

        Parameter
            name ([str], optional): [Name of database to open].
            Defaults to None.
        """
        self.connection = None
        self.cursor = None

        if name:
            self.open(name)

    def open(self, name):
        """ Opens a new database connection.

        Args:
            name ([str]): [Name of the database]
        """
        try:
            self.connection = sqlite3.connect(name)
            self.cursor = self.connection.cursor()
            print("Database open: ", name)
        except sqlite3.Error as err:
            print("Error connecting database: ", err)

    def close(self):
        """ Commit last changes and close database connection
        """
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

    def createtable(self, table, param):
        """ Create new table in database

        Args:
            table ([str]): [name of table]
            param ([str]): [comma-separated parameters for SQL CREATE TABLE]
        """
        try:
            # sqlite_create_table = """CREATE TABLE {0}(auth_id INTEGER UNIQUE,
            # author TEXT NOT NULL, PRIMARY KEY(auth_id AUTOINCREMENT))
            # """.format(table)
            sqlite_create_table = """CREATE TABLE {0}({1})""".format(table, param)
            self.cursor.execute(sqlite_create_table)
            self.connection.commit()
            print("SQLite table created:", table)

        except sqlite3.Error as err:
            print("An error occured while creating table, ", err)

    def view(self):
        self.cursor.execute("""SELECT * FROM books""")
        rows = self.cursor.fetchall()
        return rows

    def search(self, title="", author="", isbn13=""):
        self.cursor.execute("SELECT * FROM BOOKS WHERE Title=? OR Author=?", (title, author))
        rows = self.cursor.fetchall()
        return rows

    def insert(self, Title, Subtitle, Author, Publisher, PubDate, Pages, ISBN10, ISBN13, Description):
        self.cursor.execute("INSERT INTO BOOKS VALUES (NULL,?,?,?,?,?,?,?,?,?)", (Title, Subtitle, Author, Publisher, PubDate, Pages, ISBN10, ISBN13, Description))
        self.connection.commit()

    def update(self, book_id, Title, Subtitle, Author, Publisher, PubDate, Pages, ISBN10, ISBN13, Description):
        self.cursor.execute("UPDATE BOOKS SET Title=?, Subtitle=?, Author=?, Publisher=?, PubDate=?, Pages=?, ISBN10=?, ISBN13=?, Description=? WHERE book_id=?", (Title, Subtitle, Author, Publisher, PubDate, Pages, ISBN10, ISBN13, Description, book_id))
        self.connection.commit()

    def delete(self, book_id):
        self.cursor.execute("DELETE FROM BOOKS WHERE book_id=?", (book_id,))
        self.connection.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def dataframetosql(self, df_books):
        """
        Import function for pandas dataframe to Sqlite database. Overwrites
        existing entries.
        """
        df_books = pd.DataFrame
        df_books.to_sql('BOOKS', con=self.connection, if_exists='replace', index=False)

    def writesqltocsv(self):
        """Export function for database table to csv.
        """
        df_books = pd.read_sql('SELECT * FROM BOOKS', self.connection)
        df_books.to_csv('BOOK_DB.csv')

    def getdata(self, table, columns, limit=None):
        query = "SELECT {0} from {1};".format(columns, table)
        self.cursor.execute(query)
        # fetch data
        rows = self.cursor.fetchall()
        return rows[len(rows) - limit if limit else 0:]
