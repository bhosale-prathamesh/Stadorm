from django.urls import path
from . import views 

urlpatterns = [
    
    path('signup',views.signup,name='Sign Up'),
    path('details/<int:productId>/',views.details,name='Details'),
    path('',views.home,name='Home'),
    path('rooms/',views.rooms,name='Rooms'),
    path('checkout/<int:productId>/<int:length>/',views.checkout,name='Checkout'),
    path('confirmation/<int:productId>/<int:transactionId>/',views.confirmation,name='Confirmation'),
    path('subscription/',views.subscription,name='Subscription'),
]