from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns= [
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='book_list'), name='logout'),
]