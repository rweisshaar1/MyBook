from sqlalchemy.sql import func
from db.database import db
import requests
import random
from sqlalchemy.sql.expression import func
from util.globals import api_key

class Book (db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.Text, nullable=False)
    genre = db.Column(db.Text)  # New genre column
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer)
    user_rating = db.Column(db.Integer, default=0)
    status = db.Column(db.String(255))
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, book_id, image, title, author, genre, user_id, rating, user_rating, status, comment=None):
        self.book_id = book_id
        self.image = image
        self.title = title
        self.author = author
        self.genre = genre
        self.user_id = user_id
        self.rating = rating
        self.user_rating = user_rating
        self.status = status
        self.comment = comment

def add_book(book_id, image, title, authors, genre, user_id, rating, user_rating, status, comment=None):
    if rating == '' or rating is None:
        rating = 0
    if user_rating == '' or user_rating is None:
        user_rating = 0
    new_book = Book(book_id, image, title, authors, genre, user_id, rating, user_rating, status, comment=None)
    db.session.add(new_book)
    db.session.commit()
    return new_book

def get_books(user_id):
    return Book.query.filter_by(user_id=user_id).all()

def get_book_by_id(book_id):
    return Book.query.filter_by(id=book_id).first()

# will look like update_book(1, {'title': 'New Title', 'author': 'New Author'})
def update_book(book_id, updates):
    book = get_book_by_id(book_id)
    for key, value in updates.items():
        if hasattr(book, key):
            setattr(book, key, value)
    db.session.commit()
    return book

def delete_book(book_id):
    book = get_book_by_id(book_id)
    db.session.delete(book)
    db.session.commit()
    return book

# Get a number of random books from the database
def get_random_books(n):
    # Select a number of random books from the database
    books = Book.query.order_by(func.random()).limit(n).all()
    return books

# Get book recommendations for a user
def get_recommendations(user_id, n):
    # Check if there are any books in the database
    if Book.query.count() == 0:
        return []

    # Get a number of random books
    books = get_random_books(n)

    # If no books are found, return an empty list
    if not books:
        print('No books in db found')
        return []

    # Construct the queries
    queries = [f'"{book.title}"+inauthor:{book.author}' for book in books]

    # Make API calls to the Google Books API for each query
    recommended_books = []
    for query in queries:
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}')
        data = response.json()

        # Get the recommended books
        recommended_books.extend([item for item in data['items'] if item['id'] not in [book.book_id for book in Book.query.filter_by(user_id=user_id).all()]])

    # Return the recommended books
    return recommended_books