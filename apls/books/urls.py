# Django
from django.urls import path

# Views
from apls.books import views

app_name = 'book'

urlpatterns = [
    path('', views.book_index, name='index'),
]