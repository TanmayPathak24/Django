from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from .forms import AdminRegistration
from .models import Admin
from blog.views import getBlogs
from blog.models import Author, Blog
# Admin home


def admin_home(request):
    context = {}
    context['admin'] = {'avatar':getAdmin(request)}
    temp = []
    blogs = getBlogs()
    for blog in blogs:
        avatar = blog['avatar']
        id = Author.objects.filter(avatar__exact=avatar)[0].id
        blog['author_id'] = id
        temp.append(blog)
    context['blogs'] = temp
    return render(request, 'admin_home.html', context=context)

def admin_register_page(request):
    form = AdminRegistration()
    content = {
        'form': form
    }
    return render(request, 'admin_register_page.html', context=content)

def admin_register(request):
    if request.method == "POST":
        # saving the blog to the database
        admin_form = AdminRegistration(request.POST)
        if admin_form.is_valid():
            admin = Admin()
            admin.admin_name = admin_form.cleaned_data['admin_name']
            admin.avatar = admin_form.cleaned_data['avatar']
            admin.description = admin_form.cleaned_data['description']
            admin.password = admin_form.cleaned_data['password']
            admin.save()
            return HttpResponseRedirect("/Ad/home")
        else:
            error = {
                'message': 'Invalid details'
            }
            context = {
                'error':error,
                'form': admin_form
            }
            context['admin'] = {'avatar': getAdmin(request)}
            return render(request,'admin_register_page.html',context=context)


def blog_display(request, blog_id):
    blog = Blog.objects.filter(id__exact=blog_id)
    print(blog)
    temp = {
        'id': blog[0].id,
        'avatar': getAuthorAvatar(blog[0].author_id),
        'title': blog[0].title,
        'publish_date': blog[0].publish_date,
        'content': blog[0].content,
        'last_modified': blog[0].last_modified
    }
    context={}
    context['blog']=temp
    context['admin'] = {'avatar': getAdmin(request)}
    return render(request, 'admin_blog_display.html', context=context)


def user_management(request):
    context = {}
    context['users'] = getUsers()
    context['admin'] = {'avatar': getAdmin(request)}
    return render(request, 'user_management.html', context=context)

def delete_post_confirm(request, id):
    blog = Blog.objects.filter(id__exact=id)
    temp = {
        'id':blog[0].id,
        'title':blog[0].title,
        'publish_date':blog[0].publish_date
    }
    context = {}
    context['blog']=temp
    context['admin'] = {'avatar': getAdmin(request)}
    return render(request, 'admin_delete_confirm.html', context=context)

def author_profile(request, id):
    author = Author.objects.filter(id__exact=id)
    temp = {
        'id':author[0].id,
        'name':author[0].author_name,
        'avatar':author[0].avatar,
        'desc':author[0].description
    }
    context={}
    context['author'] = temp
    context['admin'] = {'avatar': getAdmin(request)}
    return render(request,'admin_author_display.html', context=context)


def delete_post(request, id):
    blog = Blog.objects.get(pk=id)
    blog.delete()
    return HttpResponseRedirect("/Ad/home")


# deleting the user
def user_remove_confirm(request, id):
    author = Author.objects.filter(id__exact=id)
    temp = {
        'id':author[0].id,
        'name':author[0].author_name,
        'avatar':author[0].avatar
    }
    context = {}
    context['user'] = temp
    context['admin'] = {'avatar': getAdmin(request)}
    return render(request, 'admin_author_delete_confirmation.html',context=context)

def user_remove(request, id):
    blogs = Blog.objects.filter(author_id__exact=id)
    for blog in blogs:
        blog.delete()
    author = Author.objects.filter(id__exact=id)
    author.delete()
    return HttpResponseRedirect("/Ad/user/management")


def getAdmin(request):
    if request.session.has_key('admin'):
        avatar = request.session['admin']
        return avatar

def getUsers():
    result = []
    users = Author.objects.all()

    for user in users:
        temp = {
            'id': user.id,
            'name': user.author_name,
            'avatar': user.avatar
        }
        result.append(temp)
    return result

def getAuthorAvatar(id):
    author = Author.objects.filter(id__exact=id)
    return author[0].avatar