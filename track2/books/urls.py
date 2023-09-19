from django import views
from django.urls import path
from .views import BookListView, BookDetailView, MyRentalListView
from . import views

urlpatterns=[
    path('', BookListView.as_view() ,name='book_list'),
    path('<int:pk>/', BookDetailView.as_view(), name= 'book_detail'),
    path('<int:pk>/review/', views.review_create, name= 'review_create'),
    path('edit_review/<int:book_id>/<int:review_id>', views.review_edit, name = 'review_edit'),
    path('delete_review/<int:book_id>/<int:review_id>', views.review_delete, name = 'review_delete'),
    path('rental/<int:book_id>', views.rental_book, name='book_rental'),
    path('my_rentals/',MyRentalListView.as_view(),name='my_rentals'),
    path('return/<int:rental_id>', views.return_book, name='book_return'),
    path('with_celery/', views.with_celery, name='c1'),
    #path('send_email/', views.send_email, name='send_email'),

]