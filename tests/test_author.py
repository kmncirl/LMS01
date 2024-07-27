import unittest
from unittest.mock import patch
from flask import Flask
from flask_restx import Api
from author import author_ns  # Import the author namespace from the author module

class AuthorResourceTestCase(unittest.TestCase):

    def setUp(self):
        # Set up Flask app and test client
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(author_ns, path='/api/author')  # Ensure the namespace path is correctly set
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    @patch('author.db.getAuthors')
    def test_get_authors(self, mock_getAuthors):
        # Mock the database response
        mock_getAuthors.return_value = ["Author 1", "Author 2"]
        
        # Make a GET request
        response = self.client.get('/api/author/get')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'authors': "['Author 1', 'Author 2']"})

    @patch('author.db.addAuthor')
    def test_add_author_success(self, mock_addAuthor):
        # Mock the database response
        mock_addAuthor.return_value = 'success'
        
        # Make a POST request
        response = self.client.post('/api/author/add', json={
            'author': 'New Author',
            'DoB': '1990-01-01'
        })
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'authors': 'Author Added New Author'})

    @patch('author.db.addAuthor')
    def test_add_author_duplicate(self, mock_addAuthor):
        # Mock the database response
        mock_addAuthor.return_value = 'duplicate'
        
        # Make a POST request
        response = self.client.post('/api/author/add', json={
            'author': 'Existing Author',
            'DoB': '1980-01-01'
        })
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'authors': 'Author already exitsExisting Author'})

if __name__ == '__main__':
    unittest.main()
