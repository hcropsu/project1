from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db import connection
from .models import BerryEntry, Comment

# Create your views here.


def entry_list(request):
    if request.method == 'POST':
        if 'add_entry' in request.POST:
            berry_type = request.POST.get('berry_type')
            amount_foraged = request.POST.get('amount_foraged')
            location = request.POST.get('location')
            new_entry = BerryEntry.objects.create(
                user=request.user, 
                berry_type=berry_type,
                amount_foraged=amount_foraged,
                location=location)
            return redirect("berries:entry_list")
        if 'berry_filter' in request.POST:
            """
            # Below is the safe way to filter the list using Django's built in database-abstraction API
            filter = request.POST.get('filter')
            entries = BerryEntry.objects.filter(berry_type = filter)
            return render(request, "berries/entry_list.html", {'entries': entries})
            """
            
            # Injection:
            # Below is an usafe way to filter the list by inserting user input to a raw SQL query.
            # Note that the HTML template 'entry_list.html' was designed to use the safe Django database API (like above)
            # so using this raw method messes up the intended rendering. If you need to get the site working
            # as intended in a safe way, you need to uncomment the "correct" for-loop in the 'entry_list.html'
            # file and delete the one that is in use for now.
            filter = request.POST.get('filter')
            query = f"SELECT user_id, berry_type, amount_foraged FROM berries_berryentry WHERE berry_type = '{filter}'"
            with connection.cursor() as cursor:
                cursor.execute(query)
                entries = cursor.fetchall()
            return render(request, "berries/entry_list.html", {'entries': entries})
            
        if 'clear_filter' in request.POST:
            entries = BerryEntry.objects.all()
            return render(request, 'berries/entry_list.html', {'entries':entries})
    entries = BerryEntry.objects.all()
    return render(request, 'berries/entry_list.html',
                  {'entries': entries})

# Broken Access Control:
# This view needs to have the '@login_required' decorator so to fix this, just uncomment it.
# Otherwise a non-logged in user can just type for example 'http://127.0.0.1:8000/berries/entry/3/' in
# the browser and see details that should be for valid logged in users only.
#@login_required(login_url='/berries/')
def entry_detail(request, entry_id):
    entry = BerryEntry.objects.get(id=entry_id)
    comments = Comment.objects.filter(entry=entry)
    return render(request, 'berries/entry_detail.html',
                  {'entry': entry, 'comments': comments})

def sign_in(request):
    try:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect("berries:entry_list")
    except:
        return render(request, "berries/entry_list.html",
                      {"error_msg":"Login failed. Please check username and password."})
    
def sign_out(request):
    logout(request)
    return redirect("berries:entry_list")

def new_comment(request, entry_id):
    if request.method == 'POST':
        entry = BerryEntry.objects.get(id=entry_id)
        text = request.POST.get('new_comment')
        Comment.objects.create(entry=entry, user=request.user, text=text)
        return redirect("berries:entry_detail", entry_id=entry_id)
    
def delete_comment(request, entry_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect("berries:entry_detail", entry_id=entry_id)