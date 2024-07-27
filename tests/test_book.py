import unittest
from unittest.mock import patch
from flask import Flask
from flask_restx import Api
from book import book_ns # Import the book namespace from the book module

class BookResourceTestCase(unittest.TestCase):

    def setUp(self):
        # Set up Flask app and test client
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(book_ns)
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    @patch('book.db.getBooks')
    def test_get_books(self, mock_getBooks):
        # Mock the database response
        mock_getBooks.return_value = ["Book 1", "Book 2"]
        
        # Make a GET request
        response = self.client.get('/book/get')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'bookDetails': "['Book 1', 'Book 2']"})

    @patch('book.db.addBook')
    def test_add_book(self, mock_addBook):
        # Mock the database response
        mock_addBook.return_value = 'success'
        
        # Make a POST request
        response = self.client.post('/book/add', json={
            'book': 'New Book',
            'authorName': 'Author Name',
            'publishedDate': '2023-01-01'
        })
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'bookDetails': 'Book Added New Book'})

    @patch('book.db.borrowedBook')
    def test_borrow_book(self, mock_borrowedBook):
        # Mock the database response
        mock_borrowedBook.return_value = 'success'
        
        # Make a POST request
        response = self.client.post('/book/borrow', json={
            'book_name': 'Book Name',
            'borrowerName': 'Borrower Name',
            'daysBorrowed': '7'
        })
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'result': 'Book borrowed Book Name by Borrower Name for 7 days.'})

if __name__ == '__main__':
    unittest.main()