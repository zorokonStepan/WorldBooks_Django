from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^authors_add/', views.authors_add, name='authors_add'),
    path('create_author/', views.create_author, name='create_author'),
    path('edit_author/<int:id>/', views.edit_author, name='edit_author'),
    path('delete_author/<int:id>/', views.delete_author, name='delete_author'),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    re_path(r'book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    re_path(r'^book/create/$', views.BookCreate.as_view(), name='book_create'),
    re_path(r'^book/update/(?P<pk>\d+)$', views.BookUpdate.as_view(), name='book_update'),
    re_path(r'^book/delete/(?P<pk>\d+)$', views.BookDelete.as_view(), name='book_delete'),
    re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    ]

