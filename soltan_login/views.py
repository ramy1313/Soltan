# Create your views here.
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def soltan_login(request):
	if request.method == 'POST':
		user = authenticate(username = request.POST['username'], password = request.POST['password'])
	else:
		user = request.user
	if user is not None:
		if user.is_active:
			login(request, user)
			messages.success(request, 'Profile details updated.',)
		else:
			messages.error(request, 'disabled account.',)
	else:
		messages.error(request, 'invalid login.',)
	return redirect('/')

def soltan_logout(request):
	logout(request)
	messages.success(request, 'Profile details updated.',)
	return redirect('/')

