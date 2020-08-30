from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Todo)
admin.site.register(Todo_Group)
admin.site.register(Settings)
