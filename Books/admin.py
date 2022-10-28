from django.contrib import admin
from .models import SKU,BooksCategory,FamousBooks

admin.site.register(BooksCategory)
admin.site.register(SKU)
admin.site.register(FamousBooks)
# Register your models here.
