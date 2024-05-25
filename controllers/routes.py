from flask import Blueprint, render_template, session
from controllers.search import search_books, search_book_by_id
from flask import request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from models.user import User
from models.book import add_book, get_books, get_recommendations

main = Blueprint('main', __name__)

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  # replace 'main.home' with your main page's endpoint

    if request.method == 'POST':
        print('POST')
        email = request.form.get('email')  
        password = request.form.get('password') 
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['email'] = email  # store the email in the session
            return redirect(url_for('main.home'))  # replace 'main.home' with your main page's endpoint
        else:
            return render_template('login/login.html', error='Invalid email or password')
    print('GET')
    return render_template('login/login.html')

# Logout route
@main.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('main.login'))

# Main route
@main.route('/')
@login_required
def home():
    books = get_books(current_user.id)
    random_book = get_recommendations(current_user.id, 2)
    print(random_book)
    return render_template('main/home.html', 
                           books=books,
                           random_books=random_book)

# Search route
@main.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('search')
    search_type = request.args.get('radioOptions')
    # print(query)
    # print(search_type)
    results = search_books(query, search_type)
    return render_template('results/search-results.html',
                           results=results)

@main.route('/book/<book_id>')
@login_required
def get_book(book_id):
    print(book_id)
    book = search_book_by_id(book_id)
    # print(book)
    return render_template('results/book.html', book=book)

# POST routes
@main.route('/addbook', methods=['POST'])
@login_required
def handler():
    title = request.form.get('title')
    book_id = request.form.get('book_id')
    image = request.form.get('image')
    authors = request.form.get('authors')
    user_id = current_user.id
    status = request.form.get('status')
    rating = request.form.get('rating')
    user_rating = request.form.get('user_rating')
    comment = request.form.get('comment')
    print("title: ", title)
    print("book_id: ", book_id)
    print("image: ", image)
    print("authors: ", authors)
    print("rating: ", rating)
    print("user_id: ", user_id)
    print("status: ", status)
    add_book(book_id, image, title, authors, user_id, rating, user_rating, status, comment)
    return redirect(url_for('main.home'))