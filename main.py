from book import book_ns
from author import author_ns
from borrower import borrower_ns
from flask import Flask, request, send_from_directory
from flask_restx import Api, Resource, fields, Namespace
from flask_cors import CORS

# Define the app and the API
app = Flask(__name__)
api = Api(app, version='1.0', title='Library management system',
          description='A simple library management system.')
# Add namespaces to the API
CORS(app)  # This will allow all origins by default

api.add_namespace(author_ns, path='/api/author')
api.add_namespace(book_ns, path='/api/book')
api.add_namespace(borrower_ns, path='/api/borrower')


@app.route('/library')
def home():
    return send_from_directory('static', 'library.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
    