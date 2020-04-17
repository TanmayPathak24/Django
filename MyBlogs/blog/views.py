from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from .models import Blog
import datetime


def home(request):
    posts = getPosts()
    context = {'posts': posts}
    # check weather user is logged in or not
    context = checkUserLogin(request, context)
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def new_blog_page(request):
    my_blog_form = BlogForm()
    context = {'form': my_blog_form}
    context = checkUserLogin(request, context)
    return render(request, 'blog/new_blog.html', context)


from .forms import BlogForm
def new_blog(request):
    if request.method == "POST":
        # saving the blog to the database
        MyBlog = BlogForm(request.POST)
        if MyBlog.is_valid():
            blog = Blog()
            blog.author_id = getUserId(request)
            blog.title = MyBlog.cleaned_data['title']
            blog.publish_date = datetime.datetime.today()
            blog.last_modified = datetime.datetime.today()
            blog.content = MyBlog.cleaned_data['content']
            blog.save()
        return HttpResponseRedirect("/")
    else:
        return render(request, 'blog/new_blog.html')


# Redirect to the blog update page
def blog_update_page(request, blog_id):
    my_blog = Blog.objects.get(pk=blog_id)
    my_blog_form = BlogForm(
        initial={
            'title': my_blog.title,
            'content': my_blog.content
        })
    return render(request, 'blog/blog_update.html', {'form': my_blog_form,'blog_id':blog_id})


def blog_update(request, blog_id):
    MyBlog = BlogForm(request.POST)
    if MyBlog.is_valid():
        blog = Blog.objects.get(pk=blog_id)
        blog.title = MyBlog.cleaned_data['title']
        blog.content = MyBlog.cleaned_data['content']
        blog.last_modified = datetime.datetime.today()
        blog.save()
    return HttpResponseRedirect("/")


# Loading the delete-confirmation block page
def delete_confirmation_page(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    content = {
        'blog_id': blog.id,
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
        'avatar':getAvatar(my_blog.author_id),
        'publish_date':my_blog.publish_date,
        'last_modified': my_blog.last_modified,
        'content':my_blog.content
    }
    return render(request, 'blog/blog_display.html', {'blog':content})


# Author signup page loading
from .forms import AuthorSignup
def signup_page(request):
    sign_up_form = AuthorSignup()
    return render(request, 'blog/signup.html', {'form':sign_up_form})

from .models import Author
def signup(request):
    sign_up_form = AuthorSignup(request.POST)
    new_author = Author()
    if sign_up_form.is_valid():
        new_author.author_name = sign_up_form.cleaned_data['author_name']
        new_author.avatar = sign_up_form.cleaned_data['avatar']
        description = sign_up_form.cleaned_data['description']
        if len(description) == 0:
            description = "No Description"
        new_author.description = description
        new_author.password = sign_up_form.cleaned_data['password']
        # save the author
        new_author.save()
    else:
        return signup_page()
    return HttpResponseRedirect("/")


from .forms import AuthorSignIn
def sign_in_page(request):
    login_form = LoginForm()
    context = {'form':login_form}
    err = getErrorMessage(request)
    if err is  not False:
        context['err'] = {'msg':err}
    return render(request, 'blog/signin.html', context)


#user & admin login
from .forms import LoginForm
from adminblock.models import Admin
def signin(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            avatar = login_form.cleaned_data['avatar']
            password = login_form.cleaned_data['password']

            admin = Admin.objects.filter(avatar__exact=avatar).filter(password__exact=password)
            if len(admin) == 1:
                # we found an admin
                setAdminToSession(request, avatar)
                return HttpResponseRedirect('/Ad/home')
            else:
                author = Author.objects.filter(avatar__exact=avatar).filter(password__exact=password)
                if len(author) == 1:
                    # we get author
                    setUserToSession(request, avatar)
                    return HttpResponseRedirect("/")
                else:
                    # setting the error message to the session
                    setErrorMessage(request, "Invalid Avatar / Password")
                    return HttpResponseRedirect('/Blog/author/signin')
        else:
            return HttpResponseRedirect("/")


def logout(request):
    if request.session.has_key('user'):
        del request.session['user']
    return HttpResponseRedirect('/')

def getAuthorIdAndAvatar():
    authors = Author.objects.all().values('id','avatar')
    output={}
    for author in authors:
        output[author['id']] = author['avatar']
    return output


from .forms import Input
def search(request):
    if request.method == 'POST':
        content = request.POST['content']
        if len(content) == 0:
            return HttpResponseRedirect("/")
        else:
            posts = getPosts(content)
            context = {'posts': posts}
            # check weather user is logged in or not
            context = checkUserLogin(request, context)
            return render(request, 'blog/home.html', context)


def blog_aulthor_display(request, avatar):
    author = Author.objects.filter(avatar__exact=avatar)
    context={}
    temp = {
        'name':author[0].author_name,
        'avatar':author[0].avatar,
        'desc':author[0].description
    }
    context['author'] = temp
    context = checkUserLogin(request, context)
    return render(request, 'blog/author_display.html', context=context)


def blog_aulthor_blog_display(request):
    author_id = getUserId(request)
    blogs = Blog.objects.filter(author_id__exact=author_id)
    posts = []
    for blog in blogs:
        temp = {
            'id': blog.id,
            'title': blog.title,
            'content': blog.content,
            'publish_date': blog.publish_date,
            'last_modified': blog.last_modified
        }
        posts.append(temp)
    context = {}
    context['blogs'] = posts
    context = checkUserLogin(request, context)
    return render(request, 'blog/blog_author_blog_display.html', context=context)


# utility functions
def getBlogs():
    posts = []
    blogs = Blog.objects.all()
    id_to_avatar = getAuthorIdAndAvatar()
    for blog in blogs:
        temp = {
            'id': blog.id,
            'avatar' :id_to_avatar[blog.author_id],
            'title': blog.title,
            'publish_date': blog.publish_date,
            'content': blog.content,
            'last_modified': blog.last_modified
        }
        posts.append(temp)
    return posts

def getPosts(*input):
    posts = []
    id_to_avatar = getAuthorIdAndAvatar()
    blogs = Blog.objects.all()

    for sample in input:
        blogs = blogs.filter(title__icontains=sample)

    for blog in blogs:
        temp = {
            'id': blog.id,
            'avatar' :id_to_avatar[blog.author_id],
            'title': blog.title,
            'publish_date': blog.publish_date,
            'content': blog.content,
            'last_modified': blog.last_modified
        }
        if len(temp['content']) > 200:
            temp['content'] = temp['content'][0:200] + " ...."
            temp['length_status'] = True
        else:
            temp['length_status'] = False
        posts.append(temp)
    return posts


def setUserToSession(request, avatar):
        request.session['user'] = avatar


def setAdminToSession(request, avatar):
    request.session['admin'] = avatar

def getUser(request):
    if request.session.has_key('user'):
        return request.session['user']
    else:
        return False

def checkUserLogin(request, input):
    if getUser(request) is not False:
        input['box'] = {'avatar':getUser(request)}
    return input

def setErrorMessage(request, err_message):
    request.session['err'] = err_message

def getErrorMessage(request):
    if request.session.has_key('err'):
        err =  request.session['err']
        del request.session['err']
        return err
    else:
        return False

def getUserId(request):
    avatar = getUser(request)
    if avatar is not None:
        return Author.objects.filter(avatar__exact=avatar).values('id')[0]['id']
    else:
        return False

def getAvatar(user_id):
    return Author.objects.get(pk=user_id).avatar

