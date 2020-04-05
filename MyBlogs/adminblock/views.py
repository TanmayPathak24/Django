from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from .forms import AdminRegistration
from .models import Admin

# Admin home
def admin_home(request):
    context = {}
    if request.session.has_key('admin'):
        avatar = request.session['admin']
        context['admin'] = {'avatar':avatar}
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
            return render(request,'admin_register_page.html',context=context)