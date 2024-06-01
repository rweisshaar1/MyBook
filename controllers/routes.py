from flask import Blueprint, render_template, session, make_response
from controllers.search import search_books, search_book_by_id
from flask import request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from models.user import User
from models.book import add_book, get_books, get_recommendations, get_book_by_id, update_book, delete_book

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
            session['email'] = email
            session['user_id'] = user.id
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            return redirect(url_for('main.home'))
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
    search_page = False
    random_book, reason = get_recommendations(2, current_user.id, search_page)
    if random_book == []:
        random_book = None
        reason = None
    
    return render_template('main/home.html', 
                           books=books,
                           saved_books=books,
                           recommended_books=random_book,
                           reason=reason)

@main.route('/recommendations')
@login_required
def recommendations():
    search_page = True
    random_book, reason = get_recommendations(2, current_user.id, search_page)
    return render_template('results/recommendations.html', 
                           recommended_books=random_book,
                           reason=reason)

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
    saved_book = get_book_by_id(current_user.id, book_id)
    return render_template('results/book.html', book=book, saved_book=saved_book)

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
    genre = request.form.get('genre')
    # print("title: ", title)
    # print("book_id: ", book_id)
    # print("image: ", image)
    # print("authors: ", authors)
    # print("rating: ", rating)
    # print("user_id: ", user_id)
    # print("status: ", status)
    add_book(book_id, image, title, authors, genre, user_id, rating, user_rating, status, comment)
    return redirect(url_for('main.home'))

@main.route('/updatebook', methods=['PUT'])
@login_required
def updating_book():
    currentUrl = request.referrer
    user_id = current_user.id
    book_id = request.form.get('book_id')
    status = request.form.get('status')
    user_rating = request.form.get('user_rating')
    comment = request.form.get('comment')
    updates = {}
    if status:
        updates['status'] = status
    
    print("url: ", currentUrl)
    print("book_id: ", book_id)
    print("updates: ", updates)
    update_book(user_id, book_id, updates)

    response = make_response("", 200)
    response.headers['HX-Redirect'] = currentUrl
    return response
    
@main.route('/removebook', methods=['DELETE'])
@login_required
def deleting_book():
    currentUrl = request.referrer
    user_id = current_user.id
    book_id = request.form.get('book_id')
    delete_book(user_id, book_id)
    
    response = make_response("", 200)
    return response

@main.route('/profile')
@login_required
def get_profile():
    books = get_books(current_user.id)
    first_name = session['first_name']

    reading = []
    want_to_read = []
    favorites = []
    have_read = []

    for book in books:
        if book.status == 'Reading':
            reading.append(book)
        elif book.status == 'Read':
            have_read.append(book)
        elif book.status == 'Favorite':
            favorites.append(book)
        elif book.status == 'Want To Read':
            want_to_read.append(book)
        
    print(reading)
    print(want_to_read)
    print("fav", favorites)
    return render_template('profile/profile.html', 
                           books=books, 
                           first_name=first_name,
                           reading=reading,
                           want_to_read=want_to_read,
                           favorites=favorites,
                           have_read=have_read)