from bookcount import count_book
from bookstore.models import Book

def count_books():
    return Book.objects.all().count()

    