import unittest
from unittest.mock import patch
from flask import Flask
from flask_restx import Api
from borrower import borrower_ns  # Import the borrower namespace from the borrower module

class BorrowerResourceTestCase(unittest.TestCase):

    def setUp(self):
        # Set up Flask app and test client
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(borrower_ns, path='/api/borrower')  # Ensure the namespace path is correctly set
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    @patch('borrower.db.getBorrowers')
    def test_get_borrowers(self, mock_getBorrowers):
        # Mock the database response
        mock_getBorrowers.return_value = ["Borrower 1", "Borrower 2"]
        
        # Make a GET request
        response = self.client.get('/api/borrower/get')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'borrowers': "['Borrower 1', 'Borrower 2']"})

    @patch('borrower.db.addBorrower')
    def test_add_borrower_success(self, mock_addBorrower):
        # Mock the database response
        mock_addBorrower.return_value = 'success'
        
        # Make a POST request
        response = self.client.post('/api/borrower/add', json={
            'borrower': 'New Borrower',
            'DoB': '1990-01-01'
        })
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'borrowers': 'Borrower Added New Borrower'})

    @patch('borrower.db.addBorrower')
    def test_add_borrower_duplicate(self, mock_addBorrower):
        # Mock the database response
        mock_addBorrower.return_value = 'duplicate'
        
        # Make a POST request
        response = self.client.post('/api/borrower/add', json={
            'borrower': 'Existing Borrower',
            'DoB': '1980-01-01'
        })
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'borrowers': 'Borrower already exitsExisting Borrower'})

    @patch('borrower.db.getBorrowedBooks')
    def test_get_borrowed_books(self, mock_getBorrowedBooks):
        # Mock the database response
        mock_getBorrowedBooks.return_value = ["Book 1", "Book 2"]
        
        # Make a POST request
        response = self.client.post('/api/borrower/borrowedBooks', json={
            'borrower': 'Borrower Name'
        })
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'borrowed_books': "['Book 1', 'Book 2']"})

if __name__ == '__main__':
    unittest.main()
