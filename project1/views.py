from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Avg,Count

from collections import Counter
from statistics import mean


from .models import Author, Book, Category, ReadingProgress,Bookmark,Note,ReadingActivity


from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

site = Site.objects.get(pk=1)
app = SocialApp.objects.get(provider="google")
app.sites.set([site])

print(Site.objects.get_current())
print(SocialApp.objects.filter(provider="google", sites=Site.objects.get_current()))

def index(request):
    authors = Author.objects.all()
    books = Book.objects.all()
    categories = Category.objects.all()
    
    categories_count = categories.count()
    books_count = books.count()
    authors_count = authors.count()
    
    context = {
        "authors":authors,
        "books":books,
        "categories":categories,
        "authors_count":authors_count,
        "books_count":books_count,
        "categories_count":categories_count
    }
    
    return render(request,"index.html",context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(
            request, username=username, password=password
        )
        
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        
        messages.error(request, "Invalid username or password")
        
    return render(request,"login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        print("========== REGISTER POST ==========")
        print(request.POST)
        
        if password != confirm_password:
            messages.error(request, "Both passwords should match")
            
            return redirect("register")
        
        if len(password)<8:
            messages.error(request,"password should have at least 8 characters long")

            return redirect("register")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exixts")
            
            return redirect("register")
        
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            
            return redirect("register")
        
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        
        login(request, user)
        
        messages.success(request, "Account created successfully")
        
        return redirect("dashboard")
    
    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def dashboard(request):
    
    return render(request, "dashboard.html", {
        "user": request.user
    })
    
def _format_minutes(minutes):
    hours, mins = divmod(minutes, 60)
    return f"{hours}h {mins}m" if hours else f"{mins}m"


def _attach_reading_helpers(entries):
    """Attach current_chapter and time_remaining_estimate onto each ReadingProgress entry."""
    for entry in entries:
        book = entry.book
        chapters = list(book.chapters.all())
        current_chapter = None
        for chapter in chapters:
            if entry.current_page >= chapter.start_page:
                current_chapter = chapter
        entry.current_chapter = current_chapter

        if book.pages:
            pages_left = max(book.pages - entry.current_page, 0)
            entry.time_remaining_estimate = _format_minutes(round(pages_left * 1.5))
        else:
            entry.time_remaining_estimate = None
    return entries


@login_required
def library(request):
    entries = list(
        ReadingProgress.objects
        .filter(user=request.user)
        .select_related("book__author", "book__category")
        .prefetch_related("book__chapters")
        .order_by("-last_read_at")
    )

    _attach_reading_helpers(entries)

    currently_reading = [e for e in entries if e.status == "reading"]
    finished = [e for e in entries if e.status == "finished"]
    saved = [e for e in entries if e.status == "saved"]

    overall_progress_percent = round(mean(e.progress_percent for e in entries)) if entries else 0

    category_counts = Counter(e.book.category.name for e in entries)
    favorite_categories = [name for name, _count in category_counts.most_common(4)]

    reading_goal_count = 12

    context = {
        "library_books": entries,
        "continuing_books": currently_reading[:3],
        "recently_added": entries[:4],
        "recently_finished": finished[:4],
        "favorite_categories": favorite_categories,
        "library_stats": {
            "currently_reading_count": len(currently_reading),
            "want_to_read_count": len(saved),
            "finished_count": len(finished),
            "overall_progress_percent": overall_progress_percent,
        },
        "reading_goal": {
            "percent": round(min(len(finished) / reading_goal_count * 100, 100)),
            "books_read": len(finished),
            "goal_count": reading_goal_count,
        },
    }
    return render(request, "library.html", context)


def _format_minutes(minutes):
    hours, mins = divmod(minutes, 60)
    return f"{hours}h {mins}m" if hours else f"{mins}m"


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(
        Book.objects.select_related("author", "category").prefetch_related("chapters"),
        id=book_id
    )

    progress, _ = ReadingProgress.objects.get_or_create(user=request.user, book=book)

    # Keep stored progress_percent in sync with current_page
    if book.pages:
        computed_pct = min(100, round((progress.current_page / book.pages) * 100))
        if computed_pct != progress.progress_percent:
            progress.progress_percent = computed_pct
            progress.save(update_fields=["progress_percent"])

    # Work out which chapter is "current" and which are complete
    chapters = list(book.chapters.all())
    current_chapter = None
    for chapter in chapters:
        if progress.current_page >= chapter.start_page:
            current_chapter = chapter
    for chapter in chapters:
        chapter.is_current = (chapter == current_chapter)
        chapter.is_complete = bool(
            current_chapter and chapter.number < current_chapter.number
        )

    bookmarks = Bookmark.objects.filter(user=request.user, book=book).select_related("chapter")
    notes = Note.objects.filter(user=request.user, book=book)
    reading_activity = ReadingActivity.objects.filter(user=request.user, book=book)[:7]

    recent_books = Book.objects.filter(
        readingprogress__user=request.user
    ).exclude(id=book.id).order_by("-readingprogress__last_read_at")[:5]

    related_books = Book.objects.filter(
        category=book.category
    ).exclude(id=book.id)[:6]

    reading_time_estimate = time_remaining = None
    if book.pages:
        reading_time_estimate = _format_minutes(round(book.pages * 1.5))  # ~1.5 min/page, adjust if you track real WPM
        pages_left = max(book.pages - progress.current_page, 0)
        time_remaining = _format_minutes(round(pages_left * 1.5))

    context = {
        "book": book,
        "progress": progress,
        "chapters": chapters,
        "current_chapter": current_chapter,
        "bookmarks": bookmarks,
        "notes": notes,
        "reading_activity": reading_activity,
        "has_bookmarks": bookmarks.exists(),
        "recent_books": recent_books,
        "related_books": related_books,
        "reading_time_estimate": reading_time_estimate,
        "time_remaining": time_remaining,
    }

    return render(request, "book_detail.html", context)
    