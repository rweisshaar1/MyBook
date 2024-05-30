from sqlalchemy.sql import func
from db.database import db
import requests
import random
from sqlalchemy.sql.expression import func
from util.globals import api_key
from controllers.search import format_data

class Book (db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.Text, nullable=False)
    genre = db.Column(db.Text)  # New genre column
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Numeric, default=0)
    user_rating = db.Column(db.Numeric, default=0)
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
    def __repr__(self):
        return f"<Book {self.book_id}: {self.title}>"

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

def get_book_by_id(user_id, book_id):
    return Book.query.filter_by(user_id=user_id).filter_by(book_id=book_id).first()

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
def get_random_books(n, user_id):
    # Select a number of random books from the database that belong to the user
    books = Book.query.filter_by(user_id=user_id).order_by(func.random()).limit(n).all()
    return books

# Get book recommendations for a user
def get_recommendations(n, user_id, search_page):
    # Check if there are any books in the database
    if Book.query.count() == 0:
        return []

    # Get a number of random books
    books = get_random_books(n, user_id)

    # If no books are found, return an empty list
    if not books:
        print('No books in db found')
        return []
        
    # Construct the reason for the recommendations
    
    # Construct the queries
    author_queries = [f'{book.author}' for book in books]
    genre_queries = [f'{book.genre}' for book in books]

    # Find the first non-empty author and genre
    author_index = 0
    while author_index < len(author_queries) and author_queries[author_index] == "":
        author_index += 1

    genre_index = 0
    while genre_index < len(genre_queries) and genre_queries[genre_index] == "":
        genre_index += 1

    # If no non-empty author or genre is found, use an empty string
    author = author_queries[author_index] if author_index < len(author_queries) else ""
    genre = genre_queries[genre_index] if genre_index < len(genre_queries) else ""

    reason = f"Because you liked {author} and {genre}"

    # Make API calls to the Google Books API for each query
    recommended_books = []
    book_titles = set()  # Keep track of the titles of the books we've already added
    for query in author_queries:
        # Get books by author
        print(query)
        response_author = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}&maxResults=40')
        data_author = response_author.json()
        for book in data_author.get('items', []):
            title = book['volumeInfo'].get('title', '')
            if title not in book_titles:
                recommended_books.append(book)
                book_titles.add(title)

    for query in genre_queries:
        # Get books by genre
        print(query)
        response_genre = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}&maxResults=40')
        data_genre = response_genre.json()
        for book in data_genre.get('items', []):
            title = book['volumeInfo'].get('title', '')
            if title not in book_titles:
                recommended_books.append(book)
                book_titles.add(title)

    # Limit the number of books to 6
    if not search_page:
        if len(recommended_books) > 6:
            recommended_books = random.sample(recommended_books, 6)

        books = format_data({'items': recommended_books})
    else:
        books = format_data({'items': recommended_books})

    # Return the recommended books
    return books, reason