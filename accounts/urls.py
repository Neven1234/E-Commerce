from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('register/',views.registerPage,name='Register'),
	path('login/',views.loginPage,name='Login'),
	path('logout/',views.logOut,name='logout'),
    path('account_settings',views.accountSettings,name='account_settings'),

    path('', views.Home,name ='Home'),
    path('user/',views.userPage,name='user-page'),
    path('products/', views.Products,name ='Products'),
    path('customers/<str:pk>/', views.Customers,name='Customers'),
    path('Update_Order/<int:item>', views.UpdateOrder,name='Update_Order'),
    path('Delete_Order/<int:item>', views.deletOrder,name='Delete_Order'),
    path('craeat-order/<int:item>', views.creatOrder,name='craeat-order'),

    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),
    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name='password_reset_confirm'),
    path('password-reset-complete/',
     auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
      name='password_reset_complete'),
]