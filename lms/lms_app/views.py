from django.shortcuts import render, redirect , get_object_or_404
from .models import *
from .forms import *

# Create your views here.

def index(request):
    if request.method == 'POST':
        add_book = BookForm(request.POST , request.FILES)
        add_Category =  CategoryForm(request.POST)
        if add_book.is_valid():
            add_book.save()
        if add_Category.is_valid():
            add_Category.save()

    x = {
        'category': Category.objects.all(),
        'books' : Book.objects.all(),
        'BookForm' : BookForm(),
        'CategoryForm' : CategoryForm(),
        'allbooks' : Book.objects.filter(active = True).count(),
        'booksold': Book.objects.filter(status = 'sold').count(),
        'bookava': Book.objects.filter(status='available').count(),
        'bookrental': Book.objects.filter(status = 'rental').count(),
    }
    return render(request , 'pages/index.html' , x)

def books(request):
    search = Book.objects.all()
    title = None
    if 'search_name' in request.GET:
        title= request.GET['search_name']
        if title:
            search = search.filter(title__icontains = title)



    x = {
        'category': Category.objects.all(),
        'books': search,
        'CategoryForm': CategoryForm(),

    }
    return render(request , 'pages/books.html' , x)





def update(request , id):
    book_id = Book.objects.get(id=id)
    if request.method == 'POST':
        book_save = BookForm(request.POST , request.FILES , instance=book_id)
        if book_save.is_valid():
            book_save.save()
            return redirect('/')
    else:
        book_save = BookForm(instance=book_id)
    context = {
        'UpdateForm' : book_save,
    }
    return render(request , 'pages/update.html' , context)

def delete(request , id):
    book_id = get_object_or_404(Book , id=id)
    if request.method == 'POST':
        book_id.delete()
        return redirect('/')
    return render(request , 'pages/delete.html')