from flask import request
from flask_restx import Namespace, Resource, fields
from sqlitedb import SQLiteDB # type: ignore

# Define the database
db = SQLiteDB()

# Define namespaces
author_ns = Namespace('author', description='Author details')

# Define models
add_model_author = author_ns.model('AuthorRequestModel', {
    'author': fields.String(required=True, description='The Author name'),
    'DoB': fields.String(required=True, description='The Author\'s date of birth'),
})

response_model_author = author_ns.model('AuthorResponseModel', {
    'authors': fields.String(description='Author details')
})

# author endpoint
@author_ns.route('/get')
class HelloResource(Resource):
    @author_ns.doc('Author Get api')
    @author_ns.marshal_with(response_model_author)
    def get(self):
        """Get the details of the authors"""
        authorsList = db.getAuthors()
        return {'authors': authorsList}

        
# author endpoints
@author_ns.route('/add')
class Ns1AddResource(Resource):
    @author_ns.expect(add_model_author)
    @author_ns.marshal_with(response_model_author)
    def post(self):
        """Add an author detail"""
        data = request.json
        result = db.addAuthor(data['author'], data['DoB'])
        if (result == 'success'):
            return {'authors': 'Author Added ' + data['author']}
        elif (result == 'duplicate'):
            return {'authors': 'Author already exits' + data['author']}
        else:
            return {'authors': 'Unkown error'}


