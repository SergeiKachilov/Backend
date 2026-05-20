from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.template import loader
from django.core.paginator import Paginator

# Create your views here.
from django.http import HttpResponse
from .models import Blog, Comment


def index(request):
    latest_blogs = Blog.objects.order_by("-pub_date").all()
    paginator = Paginator(latest_blogs, 6)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # return render(request, "index.html", {"latest_blogs": page_obj})
    template = loader.get_template("blog/index.html")
    context = {"latest_blogs": page_obj}
    return HttpResponse(template.render(context, request))

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        text = request.POST.get("comment_text")
        comment = Comment(blog=blog, comment_text=text)
        comment.save()
        return redirect("detail", blog_id= blog.id)

    
    comments = Comment.objects.filter(blog=blog).order_by("-id")

   
    
    return render(request, "blog/detail.html", {"blog": blog, "comments": comments})
