from django.contrib import admin
from .models import Blog, User, Comment

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj = None):
        return False

admin.site.register(Blog)
admin.site.register(User)
admin.site.register(Comment, CommentAdmin)