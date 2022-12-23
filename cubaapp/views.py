from django.http import request
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
import json
import base64
# Create your views here.

#-------------------------General(Dashboards,Widgets & Layout)---------------------------------------

#---------------Dashboards
@login_required(login_url="/login")
def index(request):
    context = { "breadcrumb":{"parent":"Dashboard", "child":"Dashboard"}}
    return render(request,"general/dashboard/default/index.html",context)
    

@login_required(login_url="/login")
def dashboard_02(request):
    context = { "breadcrumb":{"parent":"Dashboard", "child":"Cameras"}}
    return render(request,"general/dashboard/default/dashboard-02.html",context)
    

@login_required(login_url="/login")
def general_widget(request):
    
    images = NoFaceMaskImages.objects.all()

    if request.method == 'POST':
        items = request.POST
        start = items.get('start')
        end = items.get('end')
        print(items)
        images = NoFaceMaskImages.objects.filter(created__range=[start,end])
        print(images)

    for idx in images:
        print(idx.created)
        idx.filename = idx.filename.replace("./cubaapp/","")
    context = {"images":images}    
    return render(request,'miscellaneous/gallery/gallery-grid-desc/gallery-with-description.html',context)
    


@login_required(login_url="/login")
def chart_widget(request):
    context = { "breadcrumb":{"parent":"Dashboard", "child":"Reports"}}
    return render(request,"general/widget/chart-widget/chart-widget.html",context)
    


@login_required(login_url="/login")
def projects(request):
    context = { "breadcrumb":{"parent":"Dashboard", "child":"Settings"}}
    return render(request,"applications/projects/projects-list/projects.html",context)
    

@login_required(login_url="/login")
def projectcreate(request):
    context = { "breadcrumb":{"parent":"Dashboard", "child":"About"}}
    return render(request,"applications/projects/projectcreate/projectcreate.html",context)

#---------------------------------user
@login_required(login_url="/login")
def user_profile(request):
    context = { "breadcrumb":{"parent":"Users", "child":"User Profile"}}
    return render(request,"applications/user/user-profile/user-profile.html",context)
    

@login_required(login_url="/login")
def user_cards(request):
    context = { "breadcrumb":{"parent":"Users", "child":"User Cards"}}
    return render(request,"applications/user/user-cards/user-cards.html",context)
       

@login_required(login_url="/login")
def form_validation(request):
    context = { "breadcrumb":{"parent":"Form Controls", "child":"Validation Forms"}}
    return render(request,"forms-table/forms/form-controls/form-validation/form-validation.html",context)
    

@login_required(login_url="/login")
def base_input(request):
    context = { "breadcrumb":{"parent":"Form Controls", "child":"Base Inputs"}}
    return render(request,"forms-table/forms/form-controls/base-input/base-input.html",context)

@login_required(login_url="/login")
def lists(request):
    context = {"breadcrumb":{"parent":"Ui Kits", "child":"Lists"}}
    return render(request,'components/ui-kits/lists.html', context) 
               
#--------------------------------Buttons
@login_required(login_url="/login")
def buttons(request):
    context = {"breadcrumb":{"parent":"Buttons", "child":"Default Style"}}
    return render(request,'components/buttons/buttons.html', context)        
       
@login_required(login_url="/login")
def error_400(request):
    
    return render(request,'pages/others/error-page/error-page/error-400.html')

@login_required(login_url="/login")
def error_401(request):
    
    return render(request,'pages/others/error-page/error-page/error-401.html')
    

@login_required(login_url="/login")
def error_403(request):
    
    return render(request,'pages/others/error-page/error-page/error-403.html')
    

@login_required(login_url="/login")
def error_404(request):
    
    return render(request,'pages/others/error-page/error-page/error-404.html')
    

@login_required(login_url="/login")
def error_500(request):
    
    return render(request,'pages/others/error-page/error-page/error-500.html')
    

@login_required(login_url="/login")
def error_503(request):
    
    return render(request,'pages/others/error-page/error-page/error-503.html')
    

#----------------------------------Authentication



def sign_up(request):
    return render(request,'pages/others/authentication/sign-up/sign-up.html')  
@login_required(login_url="/login")


@login_required(login_url="/login")
def reset_password(request):
    
    return render(request,'pages/others/authentication/reset-password/reset-password.html')
    

#--------------------------------------gallery
@login_required(login_url="/login")
def gallery_grid(request):
    context = {"breadcrumb":{"parent":"Gallery", "child":"Gallery"}}    
    return render(request,'miscellaneous/gallery/gallery-grid/gallery.html',context)
    

@login_required(login_url="/login")
def grid_description(request):
    context = {"breadcrumb":{"parent":"Gallery", "child":"Gallery Grid With Description"}}    
    return render(request,'miscellaneous/gallery/gallery-grid-desc/gallery-with-description.html',context)
    

#--------------------------------------faq

@login_required(login_url="/login")
def FAQ(request):
    context = {"breadcrumb":{"parent":"FAQ", "child":"FAQ"}}    
    return render(request,'miscellaneous/FAQ/faq.html',context)
    

#---------------------------------------------------------------------------------------

@login_required(login_url="/login")
def edit_profile(request):
    form = UserForm()
    # clean up for the database incase of errors
    # User.objects.all().delete()
    user = request.user
    
    if request.method == 'POST':
        update_items = request.POST
        user_profile = User.objects.get(userid=user)
        user_profile.department = update_items.get('department')
        user_profile.address = update_items.get('address')
        user_profile.city = update_items.get('city')
        user_profile.postal = update_items.get('postal')
        user_profile.country = update_items.get('country')
        user.first_name = update_items.get('firstname')
        user.last_name = update_items.get('lastname')
        user.email = update_items.get('email')
        
        
        user.save()
        
        user_profile.save()
        # print(user_profile)

    
    try:
        user_profile = User.objects.get(userid=user)
        print('Query Available')
    except Exception as e:
        print(e)
        User.objects.create(userid=user)
        user_profile = User.objects.get(userid=user)
        
        # User Does not exist, Create a new one
    
    context = { 'user':user,'userprofile':user_profile, "breadcrumb":{"parent":"Users", "child":"User Profile"}}
    return render(request,"applications/user/edit-profile/edit-profile.html",context)

@csrf_exempt
def add_image(request):
    req = json.loads(request.body)
    imgdata = base64.b64decode(req.get('file'))
    filename = "./cubaapp/static/assets/violations/" + req.get('filename')
    # filename = req.get('filename')
    
    with open(filename, 'wb') as f:
        f.write(imgdata)
    
    NoFaceMaskImages.objects.create(filename=filename)    
    
    return HttpResponse("return this string")

    

@login_required(login_url="/login")
def to_do(request):
    tasks = Task.objects.all()
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/to_do')

    completedTasks = True
    for t in tasks:
        if t.complete == False:
            completedTasks = False

    context = {'tasks': tasks, 'form': form,'completedTasks': completedTasks, "breadcrumb":{"parent":"Todo", "child":"Todo with database"}}
    context = {'tasks': tasks, 'form': form,'completedTasks': completedTasks, "breadcrumb":{"parent":"Todo", "child":"Todo with database"}}

    return render(request,'applications/to-do/to-do.html',context)
    

@login_required(login_url="/login")
def markAllComplete(request):
    allTasks = Task.objects.all()
    for oneTask in allTasks:
        oneTask.complete = True
        oneTask.save()
    return HttpResponseRedirect("/to_do")



@login_required(login_url="/login")
def markAllIncomplete(request):
    allTasks = Task.objects.all()
    for oneTask in allTasks:
        oneTask.complete = False
        oneTask.save()
    return HttpResponseRedirect("/to_do")



@login_required(login_url="/login")
def deleteTask(request, pk):
    item = Task.objects.get(id=pk)
    item.delete()
    return HttpResponseRedirect("/to_do")



@login_required(login_url="/login")
def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    if task.complete == False:
        task.complete = True
        task.save()
    else:
        task.complete = False
        task.save()
    return HttpResponseRedirect("/to_do")

@login_required(login_url="/login")
def delete_image(request, pk):
    if request.method == "POST":
        image = NoFaceMaskImages.objects.get(id=pk)
        image.delete()
        return redirect('/images')
    
def logout_view(request):
    logout(request)
    return redirect('login')

def login_simple(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if 'next' in request.GET:
                nextPage = request.GET['next']
                print(nextPage)
                return HttpResponseRedirect(nextPage)
            else:
                return redirect('/index')
        else:
            print(form.errors)
            print('form is not valid??')
    else:
        form =AuthenticationForm()
    context = { "breadcrumb":{"parent":"Dashboard", "child":"Default"},"form":form}
    return render(request,'pages/others/authentication/login/login.html',context)

def register_simple(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('/index')
    else:
        form = UserCreationForm()
    
    return render(request,'pages/others/authentication/sign-up-simple/sign-up.html',{"form":form})
    
    
