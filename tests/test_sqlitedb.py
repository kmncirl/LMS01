import unittest
from unittest.mock import patch, MagicMock
from sqlite3 import IntegrityError
from sqlitedb import SQLiteDB # Import the SQLiteDB class from sqlitedb.py

class SQLiteDBTestCase(unittest.TestCase):

    def setUp(self):
        self.db = SQLiteDB()

    @patch('sqlitedb.sqlite3.connect')
    def test_addBook_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [[(1, 'Author Name')], []]
        
        result = self.db.addBook('New Book', 'Author Name', '2023-01-01')
        self.assertEqual(result, 'success')

    @patch('sqlitedb.sqlite3.connect')
    def test_addBook_duplicate(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        #mock_cursor.fetchall.side_effect = [[(1, 'Author Name')], IntegrityError]
        mock_cursor.fetchall.side_effect = [[(1, 'Author Name')], [(1, 'Duplicate Book')]]
        mock_cursor.execute.side_effect = [None, IntegrityError]  # Raise IntegrityError on second execute
        
        result = self.db.addBook('New Book', 'Author Name', '2023-01-01')
        self.assertEqual(result, 'duplicate')

    @patch('sqlitedb.sqlite3.connect')
    def test_addBook_author_not_found(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [[], []]
        
        result = self.db.addBook('New Book', 'Unknown Author', '2023-01-01')
        self.assertEqual(result, 'author_not_found')

    @patch('sqlitedb.sqlite3.connect')
    def test_getBooks(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, 'Book 1', '2023-01-01', 'Author 1'), (2, 'Book 2', '2023-01-02', 'Author 2')]
        
        result = self.db.getBooks()
        self.assertEqual(result, [(1, 'Book 1', '2023-01-01', 'Author 1'), (2, 'Book 2', '2023-01-02', 'Author 2')])

    @patch('sqlitedb.sqlite3.connect')
    def test_addAuthor_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        result = self.db.addAuthor('New Author', '1980-01-01')
        self.assertEqual(result, 'success')

    @patch('sqlitedb.sqlite3.connect')
    def test_addAuthor_duplicate(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = IntegrityError
        
        result = self.db.addAuthor('Existing Author', '1980-01-01')
        self.assertEqual(result, 'duplicate')

    @patch('sqlitedb.sqlite3.connect')
    def test_getAuthors(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, 'Author 1', '1980-01-01'), (2, 'Author 2', '1985-01-01')]
        
        result = self.db.getAuthors()
        self.assertEqual(result, [(1, 'Author 1', '1980-01-01'), (2, 'Author 2', '1985-01-01')])

    @patch('sqlitedb.sqlite3.connect')
    def test_addBorrower_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        result = self.db.addBorrower('New Borrower', '1990-01-01')
        self.assertEqual(result, 'success')

    @patch('sqlitedb.sqlite3.connect')
    def test_addBorrower_duplicate(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = IntegrityError
        
        result = self.db.addBorrower('Existing Borrower', '1990-01-01')
        self.assertEqual(result, 'duplicate')

    @patch('sqlitedb.sqlite3.connect')
    def test_getBorrowers(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, 'Borrower 1', '1990-01-01'), (2, 'Borrower 2', '1992-01-01')]
        
        result = self.db.getBorrowers()
        self.assertEqual(result, [(1, 'Borrower 1', '1990-01-01'), (2, 'Borrower 2', '1992-01-01')])

    @patch('sqlitedb.sqlite3.connect')
    def test_borrowedBook_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [[(1, 'Book 1')], [(1, 'Borrower 1')]]
        
        result = self.db.borrowedBook('Book 1', 'Borrower 1', 7)
        self.assertEqual(result, 'success')

    @patch('sqlitedb.sqlite3.connect')
    def test_borrowedBook_book_not_found(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [[], [(1, 'Borrower 1')]]
        
        result = self.db.borrowedBook('Unknown Book', 'Borrower 1', 7)
        self.assertEqual(result, 'book_not_found')

    @patch('sqlitedb.sqlite3.connect')
    def test_borrowedBook_borrower_not_found(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [[(1, 'Book 1')], []]
        
        result = self.db.borrowedBook('Book 1', 'Unknown Borrower', 7)
        self.assertEqual(result, 'borrower_not_found')

    @patch('sqlitedb.sqlite3.connect')
    def test_getBorrowedBooks(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('Book 1', '2023-01-01'), ('Book 2', '2023-02-01')]
        
        result = self.db.getBorrowedBooks('Borrower 1')
        self.assertEqual(result, [('Book 1', '2023-01-01'), ('Book 2', '2023-02-01')])

if __name__ == '__main__':
    unittest.main()
