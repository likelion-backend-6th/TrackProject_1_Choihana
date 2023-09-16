from celery import shared_task
from django.core.mail import send_mail
import time

from .models import Rental


@shared_task
def mock():
    time.sleep(10)

@shared_task
def book_return(rental_id):
    rental = Rental.objects.get(id=rental_id)
    subject = '책 반납완료'
    message = f'안녕하세요. 책 반납이 완료되었습니다.'\
            f'대여 도서 이름: {rental.rental_book.title} \n' \
            f'대여 아이디: {rental.id} \n' \
            f'대여자 이메일: {rental.rental_user.email} \n'\
            f'반납일자: {rental.return_date}'
    print(message)
    send_mail(subject, message, 'hanazzang999@gmail.com',[rental.rental_user.email])
