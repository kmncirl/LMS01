# Library Management System (LMS)

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

