from django.contrib import admin
from .models import Blog, Comment

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj = None):
        return False
    
    list_display=["id", "blog", "comment_text"]
    # def blog_name(self, obj):
    #     return obj.blog.blog_name
    # blog_name.short_description = 'blog_name'

# class BlogAdmin(admin.ModelAdmin):
#     list_display=("blog_name",)
# class CommentListAdmin(admin.ModelAdmin):
#     list_display=["id", "blog", "comment_text"]

admin.site.register(Blog)
# admin.site.register(User)
admin.site.register(Comment, CommentAdmin)
# admin.site.register(Blog, BlogAdmin)