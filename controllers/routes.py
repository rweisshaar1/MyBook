from flask import Blueprint, render_template, session
from controllers.search import search_books, search_book_by_id
from flask import request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from models.user import User

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
    return render_template('main/home.html')

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