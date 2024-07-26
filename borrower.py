from flask import request
from flask_restx import Namespace, Resource, fields
from sqlitedb import SQLiteDB # type: ignore

# Define the database
db = SQLiteDB()

# Define namespaces
borrower_ns = Namespace('borrower', description='Borrower details')

# Define models
add_model_borrower = borrower_ns.model('BorrowerRequestModel', {
    'borrower': fields.String(required=True, description='The Borrower name'),
    'DoB': fields.String(required=True, description='The Borrower\'s date of birth'),
})

response_model_borrower = borrower_ns.model('BorrowerResponseModel', {
    'borrowers': fields.String(description='Borrower details')
})

# Define models
add_model_borrowed_books = borrower_ns.model('BorrowedBooksRequestModel', {
    'borrower': fields.String(required=True, description='The Borrower name')
})

response_model_borrowed_books = borrower_ns.model('BorrowedBooksResponseModel', {
    'borrowed_books': fields.String(description='Borrowed books details.')
})

# borrower endpoint
@borrower_ns.route('/get')
class HelloResource(Resource):
    @borrower_ns.doc('Borrower Get api')
    @borrower_ns.marshal_with(response_model_borrower)
    def get(self):
        """Get the details of the borrowers"""
        borrowersList = db.getBorrowers()
        return {'borrowers': borrowersList}

        
# borrower endpoints
@borrower_ns.route('/add')
class Ns1AddResource(Resource):
    @borrower_ns.expect(add_model_borrower)
    @borrower_ns.marshal_with(response_model_borrower)
    def post(self):
        """Add a borrower detail"""
        data = request.json
        result = db.addBorrower(data['borrower'], data['DoB'])
        if (result == 'success'):
            return {'borrowers': 'Borrower Added ' + data['borrower']}
        elif (result == 'duplicate'):
            return {'borrowers': 'Borrower already exits' + data['borrower']}
        else:
            return {'borrowers': 'Unkown error'}
            
# borrower endpoint
@borrower_ns.route('/borrowedBooks')
class BorrowedBooksResource(Resource):
    @borrower_ns.doc('Borrowed books post api')
    @borrower_ns.expect(add_model_borrowed_books)
    @borrower_ns.marshal_with(response_model_borrowed_books)
    def post(self):
        """Post the details of the borrowers"""
        data = request.json
        borrowedBooksList = db.getBorrowedBooks(data['borrower'])
        return {'borrowed_books': borrowedBooksList}


