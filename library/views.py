from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
import requests as rs
from datetime import datetime, timedelta

def new_index(request):
    return render(request, 'index.html')

def new_book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def new_issue_book(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        book_id = request.POST.get('book_id')

        try:
            member = Member.objects.get(pk=member_id)
            book = Book.objects.get(pk=book_id)
            issue_date = datetime.now().date()

            return_date = issue_date + timedelta(days=14)

            if book.id > 0:
                transaction = Transaction(member=member, book=book, issue_date=issue_date, return_date=return_date)
                transaction.save()

                book.save()

                messages.success(request, f"Book '{book.title}' issued to {member.name}.")
            else:
                messages.error(request, f"Book '{book.title}' is not available.")
        except Member.DoesNotExist:
            messages.error(request, "Member not found.")
        except Book.DoesNotExist:
            messages.error(request, "Book not found.")

    return redirect('transaction_list')  # Updated redirect

def new_add_fine(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    if request.method == 'POST':
        fine = request.POST.get('fine')

        try:
            fine_amount = float(fine)
        except ValueError:
            messages.error(request, "Invalid fine amount. Please enter a valid number.")
            return redirect('transaction_list')  # Updated redirect

        transaction.fee = fine_amount
        transaction.save()

        messages.success(request, f"Transaction {transaction_id} has been fined ₹{fine} successfully.")
        return redirect('transaction_list')  # Updated redirect

    return redirect('transaction_list')  # Updated redirect

def new_import_books(request):
    if request.method == 'POST':
        num_books_to_import = int(request.POST.get('numberbook', 0))

        title = request.POST.get('title', '')
        authors = request.POST.get('authors', '')
        isbn = request.POST.get('isbn', '')
        publisher = request.POST.get('publisher', '')
        page = request.POST.get('page', '')

        api_url = 'https://frappe.io/api/method/frappe-library?page=2'
        params = {
            'title': title,
            'authors': authors,
            'isbn': isbn,
            'publisher': publisher,
            'page': page,
        }

        headers = {
            'Authorization': 'Bearer your_api_key_here',
        }

        try:
            response = rs.get(api_url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json().get('message', [])

                for book_data in data[:num_books_to_import]:
                    num_pages = book_data.get('num_pages', 0)

                    book = Book(
                        title=book_data['title'],
                        author=book_data['authors'],
                        isbn=book_data['isbn'],
                        publisher=book_data['publisher'],
                        page_count=num_pages,
                    )
                    book.save()

                return redirect('book_list')  # Updated redirect
            else:
                error_message = "Failed to fetch data from the API."
                return render(request, 'library/error.html', {'error_message': error_message})

        except Exception as e:
            error_message = str(e)
            return render(request, 'error.html', {'error_message': error_message})

    return render(request, 'import_book.html')

def new_delete_book(request, book_id):
    book = Book.objects.filter(pk=book_id).delete()

    if request.method == 'POST':
        messages.success(request, f"Book '{book.title}' has been deleted successfully.")
        return redirect('book_list')  # Updated redirect
    return redirect('book_list')  # Updated redirect

def new_member_list(request):
    members = Member.objects.all()
    return render(request, 'add_member.html', {'members': members})

def new_add_member(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        member = Member(name=name, email=email)
        member.save()
        messages.success(request, f"Member '{name}' added successfully.")
        return redirect('member_list')  # Updated redirect

    return redirect('member_list')  # Updated redirect

def new_delete_member(request, member_id):
    member = Member.objects.filter(pk=member_id).delete()

    if request.method == 'POST':
        messages.success(request, f"Member '{member.name}' has been deleted successfully.")
        return redirect('member_list')  # Updated redirect

    return redirect('member_list')  # Updated redirect

def new_transaction_list(request):
    transactions = Transaction.objects.all()
    members = Member.objects.all()
    books = Book.objects.all()
    context = {'members': members, 'books': books, 'transactions': transactions}
    return render(request, 'view_issued_book.html', context)
