from django.shortcuts import render


def book_index(request):
	return render(request, 'books/index_book.html', {})