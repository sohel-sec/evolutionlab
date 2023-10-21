import json
import random
from django.http import JsonResponse
from asgiref.sync import sync_to_async, async_to_sync

def books(request, **kwargs):
    # Generate a list of random books (for demonstration, you can replace this with your own data)
    random_books = [
        {"id": 1, "title": "Book 1", "author": "Author 1"},
        {"id": 2, "title": "Book 2", "author": "Author 2"},
        {"id": 3, "title": "Book 3", "author": "Author 3"},
        {"id": 4, "title": "Book 4", "author": "Author 4"},
        {"id": 5, "title": "Book 5", "author": "Author 5"}
    ]

    # You can shuffle the list to make it random
    # random.shuffle(random_books)

    # Serialize the data into JSON format
    # data = json.dumps(random_books)
    data= {'data' : random_books, 'status_code' : 200}
    # Create a JSON response
    response = JsonResponse(data, safe=False)

    return response


async def get_data():
    random_books = [
        {"id": 1, "title": "Book 1", "author": "Author 1"},
        {"id": 2, "title": "Book 2", "author": "Author 2"},
        {"id": 3, "title": "Book 3", "author": "Author 3"},
        {"id": 4, "title": "Book 4", "author": "Author 4"},
        {"id": 5, "title": "Book 5", "author": "Author 5"}
    ]
    return random_books


async def data_list(request, **kwargs):
    
    random_book = await get_data()
    print("bookjs : ", random_book)
    data= {'data' : random_book, 'status_code' : 200}

    return JsonResponse(data, safe=False)