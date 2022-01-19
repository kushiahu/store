# Django
from django.contrib import messages
from django.shortcuts import render, redirect

# Models
from apls.carts.models import Cart, CartItem
from apls.books.models import Book


# Function views
def add_item_view(request):
	if request.user.is_authenticated:
		user = request.user
	else:
		user = None

	id_uuid = request.session.get('cart_id') # None

	cart = Cart.objects.filter(id_uuid=id_uuid).first()		

	if cart is None: 
		cart = Cart.objects.create(user=user)

	request.session['cart_id'] = str(cart.id_uuid)

	if request.method == 'POST':

		book_id = request.POST.get('book_id')
		quantity = request.POST.get('quantity')

		book = Book.objects.filter(id_uuid=book_id).first()

		cart_item = CartItem.objects.filter(cart=cart, book=book).first()

		if cart_item:
			cart_item.quantity += int(quantity)
			cart_item.save()
		else:
			CartItem.objects.create(
				book=book, cart=cart,
				quantity=quantity, price=book.price
			)

		messages.info(request, f'Se ha añadido {quantity} libro del {book.name}')

		return redirect('book:detail', book.slug)

	return render(request, 'books/detail.html', {})