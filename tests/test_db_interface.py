import unittest
from abc import ABC
from db_interface import DBInterface # Import the DBInterface from db_interface module

class MockDB(DBInterface):
    def addBook(self, book_name, author_name, published_date):
        return 'success'

    def getBooks(self):
        return ['Book 1', 'Book 2']

    def addAuthor(self, author_name, date_of_birth):
        return 'success'

    def getAuthors(self):
        return ['Author 1', 'Author 2']

    def addBorrower(self, borrower_name, date_of_birth):
        return 'success'

    def getBorrowers(self):
        return ['Borrower 1', 'Borrower 2']

    def borrowedBook(self, book_name, borrowerName, daysBorrowed=30):
        return 'success'

    def getBorrowedBooks(self, borrower):
        return ['Book 1', 'Book 2']

class TestDBInterface(unittest.TestCase):
    
    def setUp(self):
        self.db = MockDB()

    def test_addBook(self):
        result = self.db.addBook('New Book', 'Author Name', '2023-01-01')
        self.assertEqual(result, 'success')

    def test_getBooks(self):
        result = self.db.getBooks()
        self.assertEqual(result, ['Book 1', 'Book 2'])

    def test_addAuthor(self):
        result = self.db.addAuthor('New Author', '1980-01-01')
        self.assertEqual(result, 'success')

    def test_getAuthors(self):
        result = self.db.getAuthors()
        self.assertEqual(result, ['Author 1', 'Author 2'])

    def test_addBorrower(self):
        result = self.db.addBorrower('New Borrower', '1990-01-01')
        self.assertEqual(result, 'success')

    def test_getBorrowers(self):
        result = self.db.getBorrowers()
        self.assertEqual(result, ['Borrower 1', 'Borrower 2'])

    def test_borrowedBook(self):
        result = self.db.borrowedBook('Book 1', 'Borrower 1', 7)
        self.assertEqual(result, 'success')

    def test_getBorrowedBooks(self):
        result = self.db.getBorrowedBooks('Borrower 1')
        self.assertEqual(result, ['Book 1', 'Book 2'])

if __name__ == '__main__':
    unittest.main()
