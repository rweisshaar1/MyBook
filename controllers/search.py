import requests
import math
import json
from util.globals import api_key
from util.globals import Truncate_String

cache = {}

def search_books(query, search_type, page):
    query = query.replace(' ', '+')

    if search_type == 'general':
        search_type = f'{query}'
    elif search_type == 'author':
        search_type = f'+inauthor:{query}'

    # Calculate the startIndex
    startIndex = (page - 1) * 12

     # Check if the results are in the cache
    cache_key = (search_type, startIndex)
    if cache_key in cache:
        return cache[cache_key]

    google_books_api_url = f'https://www.googleapis.com/books/v1/volumes?q={search_type}&key={api_key}&maxResults=12&startIndex={startIndex}'
    response = requests.get(google_books_api_url)
    data = response.json()

    total_items = data['totalItems']
    total_pages = math.ceil(total_items / 12)

    if response.status_code != 200:
        print(f"Error: API request returned status code {response.status_code}")
        return []
    if 'items' not in data:
        print("No results found")
        return []
    
    print("data: ", format_data(data))
    print("total_pages: ", total_pages)
    # Store the results in the cache
    cache[cache_key] = format_data(data), total_pages

    return format_data(data), total_pages

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