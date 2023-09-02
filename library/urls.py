from django.urls import path
from . import views

urlpatterns = [
    path('book_list/', views.new_book_list, name='book_list'),
    path('', views.new_index, name='index'),
    path('issue_book/', views.new_issue_book, name='issue_book'),
    path('delete_book/<int:book_id>/', views.new_delete_book, name='delete_book'),
    path('import/', views.new_import_books, name='import_books'),
    path('members/', views.new_member_list, name='member_list'),
    path('add_member/', views.new_add_member, name='add_member'),
    path('delete_member/<int:member_id>/', views.new_delete_member, name='delete_member'),
    path('transactions/', views.new_transaction_list, name='transaction_list'),
    path('add_fine/<int:transaction_id>/', views.new_add_fine, name='add_fine'),
]
