import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Book, Rental
from .tasks import mock, book_return
import time

# celery simple test
def with_celery(request):
    res = mock.delay()
    return HttpResponse('success')

# Create your views here.
class BookListView(ListView):
    model = Book
    context_object_name = 'books'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['books'].filter(stock__gte=1).count() #잔여수량 1개 이상인 책

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['books'] = context['books'].filter(title__icontains=search_input)
            context['search'] = search_input

        return context

class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'

    # 해당 도서를 대여중인지 확인
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        #해당 아이템의 id값
        book_id = self.kwargs['pk']
        #로그인 상태일때만 실행
        if self.request.user.is_authenticated:
            context['rental'] = Rental.objects.filter(rental_user=self.request.user, rental_book=book_id, return_date__isnull=True)
            # 오류: 대여한 도서가 없을 때, filter는 오류 발생안하는데 get으로 가져오려하면 오류 발생함
            # 해결: if문으로 대여할 도서 있을때만 get 처리
            if context['rental']:
                context['rental_id']=Rental.objects.get(rental_user=self.request.user, rental_book=book_id, return_date__isnull=True)
        return context



# 대여하기 기능 구현
def rental_book(request, book_id):
    book = Book.objects.get(id=book_id)
    user = request.user

    # 대여하기 테이블에 데이터 추가
    Rental.objects.create(rental_book=book,rental_user =user)

    # 재고 수량 -1 하기
    book.stock -= 1
    book.save()

    return render(request, 'books/rental.html',{'book':book})

def return_book(request,rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.return_date = datetime.date.today()
    rental.rental_book.stock += 1
    rental.save() # rental 업데이트
    rental.rental_book.save() #book 테이블 업데이트
    book_return.delay(rental.id)
    return render(request, 'books/return.html', {'rental':rental})



class MyRentalListView(LoginRequiredMixin,ListView):
    model = Rental
    context_object_name = 'rentals'
    template_name = 'books/myrental_list.html'

    # 로그인한 유저의 대여목록 가져오기
    def get_queryset(self):
        return Rental.objects.filter(rental_user=self.request.user)






