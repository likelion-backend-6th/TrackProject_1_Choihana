from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import NewUserForm

# Create your views here.
def register(request):

    if request.method=='POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
            return redirect('book_list')

    form = NewUserForm()
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    # def get_success_url(self):
    #     #login 성공 후 task-list 페이지로 이동
    #     return reverse_lazy('tasks')