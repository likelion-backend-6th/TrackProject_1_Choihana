from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    stock = models.PositiveIntegerField()
    summary = models.TextField()
    image = models.ImageField(upload_to='book_image/',blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Rental(models.Model):
    ## 자동 생성 필드 (외래키)
    rental_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rental_book')
    rental_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rental_user')

    ## 자동생성 외에 커스텀 필드 추가
    rental_date = models.DateField(auto_now_add=True) #최초 생성 일자
    return_date = models.DateField(null=True, blank=True) #반납 일자

    class Meta:
        ordering = ['return_date']
        #반납 없는게 위로

    def __str__(self):
        return f'{self.rental_user} rentals {self.rental_book}'