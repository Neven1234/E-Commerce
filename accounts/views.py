from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from .models import *
from .form import OrderForm,CreatUserForm , CustomerForm
from .filter import OrderFilter
from .decorators import unauthenticated_user ,allowed_users ,admin_only

# Create your views here.
@unauthenticated_user
def registerPage(req):
	# if req.user.is_authenticated:
	# 	return redirect('Home')
	# else:
	formReg=CreatUserForm()

	if req.method=='POST':
		formReg=CreatUserForm(req.POST)
		if formReg.is_valid():
			print("SIGNUP FORM IS VALID")
			user=formReg.save()
			# group=Group.objects.get(name='customer')
			# user.groups.add(group)
			# Customer.objects.create(
			# 	user=user,
			# 	)
			username=formReg.cleaned_data.get('username')
			messages.success(req,'Account was created for '+username)
			return redirect('Login')
	else :
		formReg=CreatUserForm()
	context={'formReg':formReg}
	return render(req,'accounts/register.html',context)
@unauthenticated_user
def loginPage(req):
	# if req.user.is_authenticated:
	# 	return redirect('Home')
	# else:
	context={}
	if req.method == 'POST':
		username = req.POST.get('username')
		password = req.POST.get('password')

		user=authenticate(req,username=username,password=password)
		if user is not None:
			print('logged inn')
			login(req,user)
			return redirect('Home')
		else:
			messages.info(req,'username or password is incorrect')
			return render(req,'accounts/login.html',context) 
	return render(req,'accounts/login.html',context) 

def logOut(req):
	logout(req)
	return redirect('Login')

@login_required(login_url='Login')
@admin_only
def Home(req):
	orders=Order.objects.all()
	customers=Customer.objects.all()

	
	total_customer=customers.count()
	total_orders=orders.count()
	delivered=orders.filter(status='Delivered').count()
	panding=orders.filter(status='Pending').count()

	context={'orders':orders,'customers':customers,'total_customer':total_customer,'total_orders':total_orders,'delivered':delivered,'panding':panding}
	return render(req,'accounts/dashboard.html',context)
@login_required(login_url='Login')
@allowed_users(allowed_roles=['customer'])
def userPage(req):
	orders=req.user.customer.order_set.all()
	total_orders=orders.count()
	delivered=orders.filter(status='Delivered').count()
	panding=orders.filter(status='Pending').count()
	idd=req.user.customer.id
	context={'orders':orders,'total_orders':total_orders,'delivered':delivered,'panding':panding,'idd':idd}
	print('orders',orders)
	return render(req,'accounts/user.html',context)

@login_required(login_url='Login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(req):
	customer=req.user.customer
	form=CustomerForm(instance=customer)
	if req.method=='POST':
		form=CustomerForm(req.POST,req.FILES,instance=customer)
		if form.is_valid():
			form.save()
	context={'form':form,'customer':customer}
	return render(req,'accounts/account_settings.html',context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin'])
def Products(req):
	products=Product.objects.all()
	return render(req,'accounts/product.html',{'products':products})

def Customers(req,pk):
	customer=Customer.objects.get(id=pk)
	print('cust pk is',pk)
	
	orders=customer.order_set.all()
	orders_count=orders.count()

	myFilter=OrderFilter(req.GET,queryset=orders)
	orders=myFilter.qs

	context={'customer':customer,'orders':orders,'orders_count':orders_count,'myFilter':myFilter}
	return render(req,'accounts/customer.html',context)

# @login_required(login_url='Login')
# @allowed_users(allowed_roles=['admin'])
def creatOrder(req,item):
	OrderFormSet=inlineformset_factory(Customer,Order, fields=('product','status'),extra=10)
	customer=Customer.objects.get(id=item)
	print('cust pk is',item)
	formset=OrderFormSet(queryset=Order.objects.none(), instance=customer)
	#form=OrderForm(initial={'customer':customer})
	if req.method=='POST':
		# print('POST: ',req.POST)
		#form=OrderForm(req.POST)
		formset=OrderFormSet(req.POST,instance=customer)
		if formset.is_valid():
			print('order created')
			formset.save()
			return redirect('/')
	context={'formset':formset}
	return render(req,'accounts/order_form.html',context)

# @login_required(login_url='Login')
# @allowed_users(allowed_roles=['admin'])
def UpdateOrder(req,item):
	order =Order.objects.get(id=item)
	print('the pk is :',item)
	form=OrderForm(instance=order)
	if req.method=='POST':
		# print('POST: ',req.POST)
		form=OrderForm(req.POST,instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	context={'form':form}
	return render(req,'accounts/order_form.html',context)

# @login_required(login_url='Login')
# @allowed_users(allowed_roles=['admin'])
def deletOrder(req,item):
	order =Order.objects.get(id=item)
	print('deletedpk is:',item)
	if req.method=="POST":
		order.delete()
		return redirect('/')
	context={'item':order}
	return render(req,'accounts/delete.html',context)