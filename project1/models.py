from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to="authors/", null=True)

    def __str__(self):
        return self.name

    @property
    def book_count(self):
        return self.book_set.count()

    @property
    def rating(self):
        avg = self.book_set.aggregate(avg=Avg("rating"))["avg"]
        return round(avg, 1) if avg else 0
    
class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published_date = models.DateField()
    cover = models.ImageField(upload_to="books/")

    # new fields
    pages = models.PositiveIntegerField(default=0)
    isbn = models.CharField(max_length=20, blank=True)
    language = models.CharField(max_length=50, default="English")
    publisher = models.CharField(max_length=150, blank=True)
    format = models.CharField(max_length=50, default="EPUB")
    rating = models.FloatField(default=0)
    review_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class ReadingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    current_page = models.PositiveIntegerField(default=0)
    progress_percent = models.FloatField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ("saved", "Saved"),
            ("reading", "Reading"),
            ("finished", "Finished"),
        ],
        default="saved"
    )

    last_read_at = models.DateTimeField(null=True, blank=True)



class Chapter(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="chapters")
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    start_page = models.PositiveIntegerField()
    is_locked = models.BooleanField(default=False)

    class Meta:
        ordering = ["number"]
        unique_together = ("book", "number")

    def __str__(self):
        return f"{self.book.title} — Ch. {self.number}: {self.title}"

    @property
    def progress_percent(self):
        """% complete for this chapter, based on the current user's furthest read page (if any)."""
        # Simplified placeholder — wire to per-chapter tracking if you add it later.
        return 0


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="bookmarks")
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True)
    page = models.PositiveIntegerField()
    label = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["page"]

    def __str__(self):
        return f"{self.book.title} — p.{self.page}"


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="notes")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.text[:40]


class ReadingActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reading_activity")
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="reading_activity")
    date = models.DateField(auto_now_add=True)
    pages_read = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-date"]
        unique_together = ("user", "book", "date")