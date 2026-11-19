from django.contrib import admin
from .models import Author, Book, Category, ReadingProgress, Chapter, ReadingActivity,Bookmark, Note

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(ReadingProgress)
admin.site.register(ReadingActivity)
admin.site.register(Note)
admin.site.register(Bookmark)
admin.site.register(Chapter)

