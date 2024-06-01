import requests
import json
from util.globals import api_key
from util.globals import Truncate_String

def search_books(query, search_type):
    query = query.replace(' ', '+')

    if search_type == 'general':
        search_type = f'{query}'
    elif search_type == 'author':
        search_type = f'+inauthor:{query}'

    print(search_type)

    google_books_api_url = f'https://www.googleapis.com/books/v1/volumes?q={search_type}&key={api_key}&maxResults=40'
    print(google_books_api_url)
    response = requests.get(google_books_api_url)
    data = response.json()

    if response.status_code != 200:
        print(f"Error: API request returned status code {response.status_code}")
        return []
    if 'items' not in data:
        print("No results found")
        return []
    return format_data(data)

def search_book_by_id(book_id):
    google_books_api_url = f'https://www.googleapis.com/books/v1/volumes/{book_id}?key={api_key}'
    
    response = requests.get(google_books_api_url)
    data = response.json()

    if response.status_code != 200:
        print(f"Error: API request returned status code {response.status_code}")
        return None
    return format_single_book(data)

def format_single_book(data):
    authors = ", ".join(data['volumeInfo'].get('authors', []))
    formatted_data = {
        'id': data['id'],
        'title': data['volumeInfo'].get('title', ''),
        'authors': authors,
        'description': data['volumeInfo'].get('description', ''),
        'image': data['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
        'publishedDate': data['volumeInfo'].get('publishedDate', ''),
        'publisher': data['volumeInfo'].get('publisher', ''),
        'pageCount': data['volumeInfo'].get('pageCount', ''),
        'categories': ", ".join(data['volumeInfo'].get('categories', [])),
        'rating': data['volumeInfo'].get('averageRating', ''),
    }
    return formatted_data

def format_data(data):
    formatted_data = []
    for item in data['items']:
        authors = ", ".join(item['volumeInfo'].get('authors', []))
        description = Truncate_String(item['volumeInfo'].get('description', ''), 150)
        genre = ", ".join(item['volumeInfo'].get('categories', []))  # Extract genre
        book_data = {
            'id': item['id'],
            'title': item['volumeInfo'].get('title', ''),
            'authors': authors,
            'description': description,
            'rating': item['volumeInfo'].get('averageRating', ''),
            'genre': genre,
            'image': item['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
        }
        formatted_data.append(book_data)
    return formatted_data