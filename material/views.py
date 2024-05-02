from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Ebook, Category

# Create your views here.
@login_required(login_url='login')
def ebook_list(request):
    ebooks = Ebook.objects.all()
    categories = Category.objects.all()
    
    context = { 'ebooks': ebooks, 'categories': categories }
    return render(request, 'material_test.html', context)