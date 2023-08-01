from django.http import  HttpResponse
from django.shortcuts import redirect
def unauthenticated_user(view_func):
	def wrapper_func(req,*args,**kwags):
		if req.user.is_authenticated:
			return redirect('Home')
		else:
			return view_func(req,*args,*kwags)
	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(req,*args,**kwags):

			group=None
			if req.user.groups.exists():
				group=req.user.groups.all()[0].name
			if group in allowed_roles:
				return view_func(req,*args,*kwags)
			else:
				return HttpResponse('You are not autherized to viwe this page')
		return wrapper_func
	return decorator


def admin_only(view_func):
	def wrapper_func(req,*args,**kwags):
		group=None
		if req.user.groups.exists():
			group=req.user.groups.all()[0].name

		if group=='customer':
			return redirect('user-page')

		if group=='admin':
			return view_func(req,*args,*kwags)
	return wrapper_func