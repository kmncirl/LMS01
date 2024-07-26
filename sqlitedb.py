from db_interface import DBInterface # type: ignore
import sqlite3
from datetime import datetime, timedelta

class SQLiteDB(DBInterface):
    def __init__(self):
        #self.conn = sqlite3.connect('books.db')
        #self.cursor = self.conn.cursor()
        self.db_path = 'books.db'
        self.createTable()

    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def addBook(self, book_name, author_name, published_date):
            #self.cursor.execute('INSERT INTO books (book_name, published_date) VALUES (?, ?)', (book_name, published_date))
            #self.conn.commit()
            conn = self._get_connection()
            cursor = conn.cursor()
            author_id=-1
            try:
                query = 'SELECT * FROM author WHERE author_name = ?'
                cursor.execute(query, (author_name,))
                result = cursor.fetchall()
                print(result);
                if not result:
                    return 'author_not_found';
                author_id = result[0][0]
                #return result
            finally:
                cursor.close()
                conn.close()
                
            conn1 = self._get_connection()
            cursor1 = conn1.cursor()
            print(author_id);
            try:
                cursor1.execute('INSERT INTO books (book_name, published_date,author_id) VALUES (?, ?, ?)', (book_name, published_date,author_id))
                conn1.commit()
            except sqlite3.IntegrityError:
                return 'duplicate';
            finally:
                cursor1.close()
                conn1.close()
            return 'success';

    def getBooks(self):
            #self.cursor.execute('SELECT * FROM books WHERE book_name = ?', (book_name,))
            #return self.cursor.fetchone()
            conn = self._get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT b.id AS book_id,b.book_name AS book_name, b.published_date AS published_date, a.author_name AS author_name FROM books b JOIN author a ON b.author_id = a.id;')
                result = cursor.fetchall()
                print(result);
                return result
            finally:
                cursor.close()
                conn.close()
                
    def addAuthor(self, author_name, date_of_birth):
            conn = self._get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO author (author_name, date_of_birth) VALUES (?, ?)', (author_name, date_of_birth))
                conn.commit()
            except sqlite3.IntegrityError:
                return 'duplicate';
            finally:
                cursor.close()
                conn.close()
            return 'success';

    def getAuthors(self):
            conn = self._get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM author')
                result = cursor.fetchall()
                print(result);
                return result
            finally:
                cursor.close()
                conn.close()
                
    def addBorrower(self, borrower_name, date_of_birth):
            conn = self._get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO borrower (borrower_name, date_of_birth) VALUES (?, ?)', (borrower_name, date_of_birth))
                conn.commit()
            except sqlite3.IntegrityError:
                return 'duplicate';
            finally:
                cursor.close()
                conn.close()
            return 'success';

    def getBorrowers(self):
            conn = self._get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM borrower')
                result = cursor.fetchall()
                print(result);
                return result
            finally:
                cursor.close()
                conn.close()
                
    def borrowedBook(self, book_name, borrowerName, daysBorrowed=30):
            conn = self._get_connection()
            cursor = conn.cursor()
            book_id=-1
            try:
                query = 'SELECT * FROM books WHERE book_name = ?'
                cursor.execute(query, (book_name,))
                result = cursor.fetchall()
                print(result);
                if not result:
                    return 'book_not_found';
                book_id = result[0][0]
                #return result
            finally:
                cursor.close()
                conn.close()

            print(book_id);
            
            conn1 = self._get_connection()
            cursor1 = conn1.cursor()
            borrower_id=-1
            try:
                query = 'SELECT * FROM borrower WHERE borrower_name = ?'
                cursor1.execute(query, (borrowerName,))
                result = cursor1.fetchall()
                print(result);
                if not result:
                    return 'borrower_not_found';
                borrower_id = result[0][0]
                #return result
            finally:
                cursor1.close()
                conn1.close()

            print(borrower_id);
            
            conn2 = self._get_connection()
            cursor2 = conn2.cursor()
            try:
                now = datetime.now()
                future_date = now + timedelta(days=daysBorrowed)
                cursor2.execute('INSERT INTO issued_book (book_id, borrower_id,borrower_date,return_date) VALUES (?, ?, ?, ?)', (book_id, borrower_id,now.strftime('%Y-%m-%d'),future_date.strftime('%Y-%m-%d')))
                conn2.commit()
            except sqlite3.IntegrityError:
                return 'duplicate';
            finally:
                cursor2.close()
                conn2.close()
            return 'success';
            
    def getBorrowedBooks(self,borrower):
            conn = self._get_connection()
            cursor = conn.cursor()
            try:
                query = 'SELECT b.book_name, ib.return_date FROM issued_book ib JOIN books b ON ib.book_id = b.id JOIN borrower br ON ib.borrower_id = br.id WHERE br.borrower_name = ?'
                cursor.execute(query, (borrower,))
                result = cursor.fetchall()
                print(result);
                return result
            finally:
                cursor.close()
                conn.close()

    #def __del__(self):
    #    self.conn.close()

    def createTable(self):
        #self.cursor.execute(''' CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, book_name TEXT NOT NULL, published_date DATE NOT NULL)''')
        #self.conn.commit()
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(''' CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, book_name TEXT NOT NULL UNIQUE, published_date TEXT NOT NULL, author_id INTEGER)''')
            cursor.execute(''' CREATE TABLE IF NOT EXISTS author (id INTEGER PRIMARY KEY, author_name TEXT NOT NULL UNIQUE, date_of_birth TEXT NOT NULL)''')
            cursor.execute(''' CREATE TABLE IF NOT EXISTS borrower (id INTEGER PRIMARY KEY, borrower_name TEXT NOT NULL UNIQUE, date_of_birth TEXT NOT NULL)''')
            cursor.execute(''' CREATE TABLE IF NOT EXISTS issued_book (book_id INTEGER, borrower_id INTEGER TEXT, borrower_date TEXT NOT NULL, return_date TEXT NOT NULL)''')
            conn.commit()
            #return result
        finally:
            cursor.close()
            conn.close()
    