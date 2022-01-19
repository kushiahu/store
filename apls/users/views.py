# Django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Forms
from apls.users.forms import LoginForm


def login_view(request):
	if request.user.is_authenticated:
		return redirect('/')

	form = LoginForm(request.POST or None)

	if request.method == 'POST' and form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('/')

	ctx = {
		'form': form
	}
	return render(request, 'users/auth/login.html', ctx)


def logout_view(request):
	logout(request)
	return redirect('book:index')