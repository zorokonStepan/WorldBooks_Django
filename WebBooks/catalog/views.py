from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import AuthorsForm
from .models import Book, Author, BookInstance, Genre

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Универсальный класс представления списка книг, находящихся в заказе у текущего пользователя."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='2').order_by('due_back')


class BookListView(generic.ListView):
    model = Book
    paginate_by = 3


class BookDetailView(generic.DetailView):
    model = Book


class BookCreate(CreateView):
    """перенаправляют пользователя на страницу, указанную в параметре success_url.
    Эта страница, на которую будет перенаправлен пользователь в случае успешного завершения операции,
    покажет ему созданные или отредактированные данные. Кстати, при помощи параметра
    success_url можно задать и альтернативное перенаправление

    Здесь с параметром success_url мы используем функцию reverse_lazy() -
    для перехода на страницу списка книг.
    Функция reverse_lazy() - это более «ленивая» версия функции reverse()."""
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4


def index(request):
    # Генерация "количеств" некоторых главньх объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'На складе')
    # Здесь метод 'all()' применен по умолчанию.
    num_instances_available = BookInstance.objects.filter(status__exact=2).count()
    # Авторы книг,
    num_authors = Author.objects.count()

    # Количество посещений этого view, подсчитанное в переменной session
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка НТМL-шаблона index.html с данными внутри переменной context
    return render(request, 'catalog/index.html',
                  context={'num_books': num_books,
                           'num_instances': num_instances,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors,
                           'num_visits': num_visits,
                           }
                  )


def authors_add(request):
    """получение данных из БД и загрузка шаблона authors add.html """
    authors = Author.objects.all()
    authors_form = AuthorsForm()
    return render(request,
                  "catalog/authors_add.html",
                  {"form": authors_form, "authors": authors}
                  )


def create_author(request):
    """сохранение данных об авторах в БД """
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect('/catalog/authors_add/')


def edit_author(request, id):
    """изменение данных в БД """
    author = Author.objects.get(id=id)
    if request.method == "POST":
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/catalog/authors_add/")
    else:
        return render(request, "catalog/edit_author.html", {"author": author})


def delete_author(request, id):
    """удаление авторов иэ БД """
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect("/catalog/authors_add/")
    except Author.DoesNotExist:
        return HttpResponseNotFound("<h2>Aвтop не найден</h2>")
