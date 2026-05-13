from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.template import loader

# Create your views here.
from django.http import HttpResponse
from .models import Blog, Comment


def index(request):
    latest_blogs = Blog.objects.order_by("-pub_date")
    template = loader.get_template("blog/index.html")
    context = {"latest_blogs": latest_blogs}
    return HttpResponse(template.render(context, request))

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog).order_by("-id")

    if request.method == "POST":
        text = request.POST.get("comment_text")
        comment = Comment(blog=blog, comment_text=text)
        comment.save()
    
    return render(request, "blog/detail.html", {"blog": blog, "comments": comments})
