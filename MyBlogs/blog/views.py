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
    sign_in_form = AuthorSignIn()
    context = {'form':sign_in_form}
    err = getErrorMessage(request)
    if err is  not False:
        context['err'] = {'msg':err}
    return render(request, 'blog/signin.html', context)


def signin(request):
    sing_in_form = AuthorSignIn(request.POST)
    if sing_in_form.is_valid():
        # check for the user in the database
        user_avatar = sing_in_form.cleaned_data['avatar']
        user_password = sing_in_form.cleaned_data['password']
        filter = Author.objects.filter(avatar__exact=user_avatar).filter(password__exact=user_password)
        if len(filter) == 1:
            setUserToSession(request, user_avatar)
            return HttpResponseRedirect("/")
        else:
            # setting the error message to the session
            setErrorMessage(request, "Invalid Avatar / Password")
            return HttpResponseRedirect('/Blog/author/signin')


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
    content = Input(request.POST)
    print(content)
    if content.is_valid():
        print("-------------------------------------------------------")
        print(content)
    return HttpResponseRedirect("/")

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

def setUserToSession(request, avatar):
        request.session['user'] = avatar

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