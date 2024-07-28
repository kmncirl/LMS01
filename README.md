# Library Management System (LMS)
### Overview
The Library Management System (LMS) is a RESTful web service application developed using Python, Flask web framework, SQLite in-memory database. It is used to manage authors, books, borrowers. It allows you to add new books, authors and borrowers, borrow books, retrieve details of the books, authors, borrowers and borrowed books. 

## Pre-requisite and Installation
- Download and install Python from https://www.python.org/downloads/
- Install other python dependencies for this project -> Flask, flask-restx, flask-restful, flask-cors, flasgger, requests.
- The above dependencies can be installed using requirements.txt.
- ### requirements.txt
  ```sh
  Flask
  flask-restx
  flask-restful
  flask-cors
  flasgger
  requests
  ```
- ```sh
  pip install -r requirements.txt
  ```
- You can also install the above dependencies separately from the command line using pip using the following commands instead of the above requirements.txt file.
- ```sh
  pip install Flask
  pip install flask-restx
  pip install flask-restful
  pip install flask-cors
  pip install flasgger
  pip install requests
  ```
- Note: sqlite3 and unittest are part of the Python Standard Library and hence does not need to be installed separately with pip.

## Setup and Running the Application
1. Clone the repository:
```sh
git clone https://github.com/kmncirl/LMS01.git
```

2. Navigate into the project diretcory:
```sh
cd LMS01
```

3. Run the application:
```sh
python main.py
```

4. Run Unit tests:
```sh
python -m unittest discover tests
```   

5. Run Integration tests:
```sh
python test_integration.py
```   

## LMS - Static HTML WebPage/UI
- Open any web browser. (ex: Chrome, Firefox, Brave, etc.)
- Navigate to the following URL - http://localhost:5000/static/library.html
- Play around our Library Management System (LMS) application.

## API documentation
### Swagger UI 
- Open any web browser and navigate to the following URL http://localhost:5000/
- You can find the various details such as API endpoints (Book, Author, Borrower endpoints), API Request and Response models.
- Also, you can execute API tests by using the "Try it out" option on the swagger UI.

### API Endpoints
- **Author Endpoint**
  - Add Author: POST /api/author/add
  - Get Authors: GET /api/author/get

- **Book Endpoint**
  - Add Book: POST /api/book/add
  - Get Books: GET /api/book/get
  - Borrow Book: POST /api/book/borrow

- **Borrower Endpoint**
  - Add Borrower: POST /api/borrower/add
  - Get Borrowers: GET /api/borrower/get
  - Borrowed Books: POST /api/borrower/borrowedBooks

### API Request Response Models
- **Author Request Model**
```json
{
  "type": "object",
  "required": [
    "DoB",
    "author"
  ],
  "properties": {
    "author": {
      "type": "string",
      "description": "The Author name"
    },
    "DoB": {
      "type": "string",
      "description": "The Author's date of birth"
    }
  }
}
```
- **Author Response Model**
```json
{
  "type": "object",
  "properties": {
    "authors": {
      "type": "string",
      "description": "Author details"
    }
  }
}
```
- **Book Request Model**
```json
{
  "type": "object",
  "required": [
    "authorName",
    "book",
    "publishedDate"
  ],
  "properties": {
    "book": {
      "type": "string",
      "description": "The book name"
    },
    "authorName": {
      "type": "string",
      "description": "Name of the author of the book"
    },
    "publishedDate": {
      "type": "string",
      "description": "The book published date"
    }
  }
}
```
- **Book Response Model**
```json
{
  "type": "object",
  "properties": {
    "bookDetails": {
      "type": "string",
      "description": "Book details"
    }
  }
}
```
- **Borrow Book Request Model**
```json
{
  "type": "object",
  "required": [
    "book_name",
    "borrowerName",
    "daysBorrowed"
  ],
  "properties": {
    "book_name": {
      "type": "string",
      "description": "The book name"
    },
    "borrowerName": {
      "type": "string",
      "description": "The person who borrows the book"
    },
    "daysBorrowed": {
      "type": "string",
      "description": "The number of days borrowed"
    }
  }
}
```
- **Borrow Book Response Model**
```json
{
  "type": "object",
  "properties": {
    "result": {
      "type": "string",
      "description": "Borrow book result"
    }
  }
}
```
- **Borrower Request Model**
```json
{
  "type": "object",
  "required": [
    "DoB",
    "borrower"
  ],
  "properties": {
    "borrower": {
      "type": "string",
      "description": "The Borrower name"
    },
    "DoB": {
      "type": "string",
      "description": "The Borrower's date of birth"
    }
  }
}
```
- **Borrower Response Model**
```json
{
  "type": "object",
  "properties": {
    "borrowers": {
      "type": "string",
      "description": "Borrower details"
    }
  }
}
```
- **Borrowed Books Request Model**
```json
{
  "type": "object",
  "required": [
    "borrower"
  ],
  "properties": {
    "borrower": {
      "type": "string",
      "description": "The Borrower name"
    }
  }
}
```
- **Borrowed Books Response Model**
```json
{
  "type": "object",
  "properties": {
    "borrowed_books": {
      "type": "string",
      "description": "Borrowed books details."
    }
  }
}
```
 
## Database Schema
The database schema includes the following tables:
- **author** table stores author details.
  - id: Primary key, integer, unique identifier for each author.
  - author_name: Text, name of the author, must be unique.
  - date_of_birth: Text, date of birth of the author.
```sql
CREATE TABLE IF NOT EXISTS author (
    id INTEGER PRIMARY KEY, 
    author_name TEXT NOT NULL UNIQUE, 
    date_of_birth TEXT NOT NULL
);
``` 
- **books** table stores book details.
  - id: Primary key, integer, unique identifier for each book.
  - book_name: Text, name of the book, must be unique.
  - published_date: Text, publication date of the book.
  - author_id: Integer, foreign key referencing the author table.
```sql
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY, 
    book_name TEXT NOT NULL UNIQUE, 
    published_date TEXT NOT NULL, 
    author_id INTEGER
);
```
- **borrower** table stores borrower details.
  - id: Primary key, integer, unique identifier for each borrower.
  - borrower_name: Text, name of the borrower, must be unique.
  - date_of_birth: Text, date of birth of the borrower.
```sql
CREATE TABLE IF NOT EXISTS borrower (
    id INTEGER PRIMARY KEY, 
    borrower_name TEXT NOT NULL UNIQUE, 
    date_of_birth TEXT NOT NULL
);
```
- **issued_book** table stores issued book details.
  - book_id: Integer, foreign key referencing the books table.
  - borrower_id: Integer, foreign key referencing the borrower table.
  - borrower_date: Text, date when the book was borrowed.
  - return_date: Text, date when the book is expected to be returned.
```sql
CREATE TABLE IF NOT EXISTS issued_book (
    book_id INTEGER, 
    borrower_id INTEGER, 
    borrower_date TEXT NOT NULL, 
    return_date TEXT NOT NULL
);
```  
    

