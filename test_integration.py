import unittest
from flask import Flask
from flask_restx import Api
from main import app
from sqlitedb import SQLiteDB
import json

class TestLibraryManagementSystem(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True
        cls.db = SQLiteDB()
        cls.db.createTable()
    
    def tearDown(self):
        # Clear the database entries after each test
        conn = self.db._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM issued_book')
            cursor.execute('DELETE FROM books')
            cursor.execute('DELETE FROM author')
            cursor.execute('DELETE FROM borrower')
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def test_add_author(self):
        # Test adding a new author
        author_data = {
            "author": "J.K. Rowling",
            "DoB": "1965-07-31"
        }
        response = self.app.post('/api/author/add', data=json.dumps(author_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Author Added', response.json['authors'])
        
        # Test adding a duplicate author
        response = self.app.post('/api/author/add', data=json.dumps(author_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Author already exits', response.json['authors'])

    def test_add_book(self):
        # Add a new author first
        author_data = {
            "author": "George Orwell",
            "DoB": "1903-06-25"
        }
        self.app.post('/api/author/add', data=json.dumps(author_data), content_type='application/json')
        
        # Test adding a new book
        book_data = {
            "book": "1984",
            "authorName": "George Orwell",
            "publishedDate": "1949-06-08"
        }
        response = self.app.post('/api/book/add', data=json.dumps(book_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book Added', response.json['bookDetails'])
        
        # Test adding a duplicate book
        response = self.app.post('/api/book/add', data=json.dumps(book_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book already exits', response.json['bookDetails'])
        
        # Test adding a book with an author that does not exist
        book_data = {
            "book": "Animal Farm",
            "authorName": "Non Existent Author",
            "publishedDate": "1945-08-17"
        }
        response = self.app.post('/api/book/add', data=json.dumps(book_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Create author first', response.json['bookDetails'])
    
    def test_add_borrower(self):
        # Test adding a new borrower
        borrower_data = {
            "borrower": "John Doe",
            "DoB": "1990-01-01"
        }
        response = self.app.post('/api/borrower/add', data=json.dumps(borrower_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Borrower Added', response.json['borrowers'])
        
        # Test adding a duplicate borrower
        response = self.app.post('/api/borrower/add', data=json.dumps(borrower_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Borrower already exits', response.json['borrowers'])

    def test_borrow_book(self):
        # Add a new author first
        author_data = {
            "author": "George Orwell",
            "DoB": "1903-06-25"
        }
        self.app.post('/api/author/add', data=json.dumps(author_data), content_type='application/json')
        
        # Add a new book
        book_data = {
            "book": "1984",
            "authorName": "George Orwell",
            "publishedDate": "1949-06-08"
        }
        self.app.post('/api/book/add', data=json.dumps(book_data), content_type='application/json')
        
        # Add a new borrower
        borrower_data = {
            "borrower": "John Doe",
            "DoB": "1990-01-01"
        }
        self.app.post('/api/borrower/add', data=json.dumps(borrower_data), content_type='application/json')
        
        # Test borrowing a book
        borrow_data = {
            "book_name": "1984",
            "borrowerName": "John Doe",
            "daysBorrowed": "30"
        }
        response = self.app.post('/api/book/borrow', data=json.dumps(borrow_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book borrowed', response.json['result'])
        
        # Test borrowing a non-existent book
        borrow_data = {
            "book_name": "Non Existent Book",
            "borrowerName": "John Doe",
            "daysBorrowed": "30"
        }
        response = self.app.post('/api/book/borrow', data=json.dumps(borrow_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book not found', response.json['result'])
        
        # Test borrowing a book with a non-existent borrower
        borrow_data = {
            "book_name": "1984",
            "borrowerName": "Non Existent Borrower",
            "daysBorrowed": "30"
        }
        response = self.app.post('/api/book/borrow', data=json.dumps(borrow_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Borrower not found', response.json['result'])

    def test_get_borrower_details(self):
        # Add a new borrower
        borrower_data = {
            "borrower": "John Doe",
            "DoB": "1990-01-01"
        }
        self.app.post('/api/borrower/add', data=json.dumps(borrower_data), content_type='application/json')
        
        # Test retrieving borrower details
        response = self.app.get('/api/borrower/get')
        self.assertEqual(response.status_code, 200)
        self.assertIn('John Doe', response.json['borrowers'])

    def test_get_borrowed_books(self):
        # Add a new author first
        author_data = {
            "author": "George Orwell",
            "DoB": "1903-06-25"
        }
        self.app.post('/api/author/add', data=json.dumps(author_data), content_type='application/json')
        
        # Add a new book
        book_data = {
            "book": "1984",
            "authorName": "George Orwell",
            "publishedDate": "1949-06-08"
        }
        self.app.post('/api/book/add', data=json.dumps(book_data), content_type='application/json')
        
        # Add a new borrower
        borrower_data = {
            "borrower": "John Doe",
            "DoB": "1990-01-01"
        }
        self.app.post('/api/borrower/add', data=json.dumps(borrower_data), content_type='application/json')
        
        # Borrow a book
        borrow_data = {
            "book_name": "1984",
            "borrowerName": "John Doe",
            "daysBorrowed": "30"
        }
        self.app.post('/api/book/borrow', data=json.dumps(borrow_data), content_type='application/json')
        
        # Test retrieving borrowed books for a borrower
        borrowed_books_data = {
            "borrower": "John Doe"
        }
        response = self.app.post('/api/borrower/borrowedBooks', data=json.dumps(borrowed_books_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('1984', response.json['borrowed_books'])

if __name__ == '__main__':
    unittest.main()
