from django.contrib import admin
from .models import Student

# ចុះឈ្មោះ Model ទាំងអស់ដើម្បីឱ្យវាបង្ហាញក្នុង Admin Panel
admin.site.register(Student)

# Register your models here.
