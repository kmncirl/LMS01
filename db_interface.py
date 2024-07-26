from abc import ABC, abstractmethod

class DBInterface(ABC):
    @abstractmethod
    def addBook(self):
        pass

    @abstractmethod
    def getBooks(self):
        pass
        
    @abstractmethod
    def addAuthor(self):
        pass

    @abstractmethod
    def getAuthors(self):
        pass
        
    @abstractmethod
    def addBorrower(self):
        pass

    @abstractmethod
    def getBorrowers(self):
        pass
        
    @abstractmethod
    def borrowedBook(self):
        pass

    @abstractmethod
    def getBorrowedBooks(self):
        pass
