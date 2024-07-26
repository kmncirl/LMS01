from flask import request
from flask_restx import Namespace, Resource, fields
from sqlitedb import SQLiteDB # type: ignore

# Define the database
db = SQLiteDB()

# Define namespaces
book_ns = Namespace('book', description='Book operations')

# Define models
add_model_book = book_ns.model('BookRequestModel', {
    'book': fields.String(required=True, description='The book name'),
    'authorName': fields.String(required=True, description='Name of the author of the book'),
    'publishedDate': fields.String(required=True, description='The book published date')
})

response_model_book = book_ns.model('BookResponseModel', {
    'bookDetails': fields.String(description='Book details')
})

add_model_borrow_book = book_ns.model('BorrowBookRequestModel', {
    'book_name': fields.String(required=True, description='The book name'),
    'borrowerName': fields.String(required=True, description='The person who borrows the book'),
    'daysBorrowed': fields.String(required=True, description='The number of days borrowed')
})

response_model_borrow_book = book_ns.model('BorrowBookResponseModel', {
    'result': fields.String(description='Borrow book result')
})

# Book endpoint
@book_ns.route('/get')
class HelloResource(Resource):
    @book_ns.doc('Book get api')
    @book_ns.marshal_with(response_model_book)
    def get(self):
        """Get all book details"""
        booksList = db.getBooks()
        return {'bookDetails': booksList}

        
# Book endpoints
@book_ns.route('/add')
class Ns1AddResource(Resource):
    @book_ns.expect(add_model_book)
    @book_ns.marshal_with(response_model_book)
    def post(self):
        """Add a new book"""
        data = request.json
        result = db.addBook(data['book'], data['authorName'], data['publishedDate'])
        if (result == 'success'):
            return {'bookDetails': 'Book Added ' + data['book']}
        elif (result == 'duplicate'):
            return {'bookDetails': 'Book already exits' + data['book']}
        elif (result == 'author_not_found'):
            return {'bookDetails': 'Create author first. Book author not found for author.' + data['authorName']}
        else:
            return {'bookDetails': 'Unkown error'}
            
# Book endpoints
@book_ns.route('/borrow')
class BorrowBookResource(Resource):
    @book_ns.expect(add_model_borrow_book)
    @book_ns.marshal_with(response_model_borrow_book)
    def post(self):
        """Borrow a book"""
        data = request.json
        result = db.borrowedBook(data['book_name'], data['borrowerName'], int(data['daysBorrowed']))
        if (result == 'success'):
            return {'result': 'Book borrowed ' + data['book_name'] + ' by '+data['borrowerName'] +' for ' +data['daysBorrowed'] +' days.'}
        elif (result == 'book_not_found'):
            return {'result': 'Book not found exits' + data['book_name']}
        elif (result == 'borrower_not_found'):
            return {'result': 'Borrower not found exits.' + data['borrowerName']}
        else:
            return {'result': 'Unkown error'}


