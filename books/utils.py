from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from random import sample

from books.models import Book


def paginateBooks(request, queryset, results):
    page = request.GET.get("page")  # current page we are on

    paginator = Paginator(queryset, results)

    try:
        # presenting only results of the requested page
        queryset = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        queryset = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        queryset = paginator.page(page)

    leftIndex = int(page) - 2
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 2
    if rightIndex < 5:
        rightIndex = 5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(leftIndex, rightIndex + 1)
    return custom_range, queryset


def searchBooks(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")
    books = Book.objects.distinct().filter(
        Q(title__icontains=search_query)
        | Q(description__icontains=search_query)
        | Q(author__icontains=search_query)
    )
    return books, search_query


def getRandomBooks(numOfBooks):
    """Return list of random books in length of numOfBooks"""
    book_pks = list(Book.objects.values_list("pk", flat=True))
    random_pks = sample(book_pks, min(numOfBooks, len(book_pks)))
    random_books = Book.objects.filter(pk__in=random_pks)
    return list(random_books)
