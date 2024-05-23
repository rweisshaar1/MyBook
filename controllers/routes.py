from flask import Blueprint, render_template
from controllers.search import search_books, search_book_by_id
from flask import request

main = Blueprint('main', __name__)

# Main route
@main.route('/')
def hello_world():
    return render_template('main/home.html')

# Search route
@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('search')
    search_type = request.args.get('radioOptions')
    print(query)
    print(search_type)
    results = search_books(query, search_type)
    return render_template('results/search-results.html',
                           results=results)

@main.route('/book/<book_id>')
def get_book(book_id):
    print(book_id)
    book = search_book_by_id(book_id)
    print(book)
    return render_template('results/book.html', book=book)