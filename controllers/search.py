import requests
import json
from util.globals import api_key
from util.globals import Truncate_String

def search_books(query, search_type):
    if search_type == 'title':
        search_type = f'intitle:{query}'
    elif search_type == 'author':
        search_type = f'inauthor:{query}'

    google_books_api_url = f'https://www.googleapis.com/books/v1/volumes?q={search_type}&key={api_key}'
    
    response = requests.get(google_books_api_url)
    data = response.json()

    print(data)

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
    return data

def format_data(data):
    formatted_data = []
    for item in data['items']:
        authors = ", ".join(item['volumeInfo'].get('authors', []))
        description = Truncate_String(item['volumeInfo'].get('description', ''), 150)
        formatted_data.append({
            'id': item['id'],
            'title': item['volumeInfo'].get('title', ''),
            'authors': authors,
            'description': description,
            'image': item['volumeInfo'].get('imageLinks', {}).get('thumbnail', '')
        })
    return formatted_data