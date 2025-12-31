from django.contrib import admin
from .models import Blog, Comment, Reaction, Contact

# Register your models here.


# @admin.register(Blog)
# class BlogAdmin(admin.ModelAdmin):
#     list_display = ('title', 'created_at')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_at')

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('blog', 'reaction_type')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
