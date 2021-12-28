from django.contrib import admin
from .models import User, Note
# Register your models here.


@admin.register(User)
class ModelAdminUser(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff',
                    'is_superuser', 'is_validated', 'is_active']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'writter', 'written_by']
