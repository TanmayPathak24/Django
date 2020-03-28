from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from .models import Blog
import datetime


def home(request):
    posts = getBlogs()
    temp = []
    # filter the posts on the basis on their content length
    for post in posts:
        if len(post['content']) > 200:
            post['content'] = post['content'][0:200] + " ...."
            post['length_status'] = True
        else:
            post['length_status'] = False
        temp.append(post)

    posts = temp
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def new_blog_page(request):
    my_blog_form = BlogForm()
    return render(request, 'blog/new_blog.html', {'form': my_blog_form})


from .forms import BlogForm
def new_blog(request):
    if request.method == "POST":
        # saving the blog to the database
        MyBlog = BlogForm(request.POST)
        if MyBlog.is_valid():
            blog = Blog()
            blog.author = MyBlog.cleaned_data['author']
            blog.title = MyBlog.cleaned_data['title']
            blog.publish_date = datetime.date.today()
            blog.content = MyBlog.cleaned_data['content']
            blog.save()

        return HttpResponseRedirect("/")
    else:
        return render(request, 'blog/new_blog.html')


def blog_update_page(request, blog_id):
    my_blog = Blog.objects.get(pk=blog_id)
    my_blog_form = BlogForm(
        initial={'author': my_blog.author, 'title': my_blog.title, 'content': my_blog.content})
    return render(request, 'blog/blog_update.html', {'form': my_blog_form, 'blog_id': my_blog.id})


def blog_update(request, blog_id):
    MyBlog = BlogForm(request.POST)
    if MyBlog.is_valid():
        blog = Blog.objects.get(pk=blog_id)
        blog.author = MyBlog.cleaned_data['author']
        blog.title = MyBlog.cleaned_data['title']
        blog.content = MyBlog.cleaned_data['content']
        blog.save()
    return HttpResponseRedirect("/")


# Loading the delete-confirmation block page
def delete_confirmation_page(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    content = {
        'blog_id': blog.id,
        'author': blog.author,
        'title': blog.title,
        'publish_date': blog.publish_date
    }
    return render(request, 'blog/delete_confirm.html', {'content': content})


# Function to delete the post
def delete_post(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    blog.delete()
    return HttpResponseRedirect("/")


# Function to display the post
def display_post(request, blog_id):
    my_blog = Blog.objects.get(pk=blog_id)
    content = {
        'blog_id':my_blog.id,
        'title':my_blog.title,
        'author':my_blog.author,
        'publish_date':my_blog.publish_date,
        'content':my_blog.content
    }
    return render(request, 'blog/blog_display.html', {'blog':content})



# utility functions
def getBlogs():
    posts = []
    blogs = Blog.objects.all()
    for blog in blogs:
        temp = {
            'id': blog.id,
            'author': blog.author,
            'title': blog.title,
            'publish_date': blog.publish_date,
            'content': blog.content
        }
        posts.append(temp)
    return posts
