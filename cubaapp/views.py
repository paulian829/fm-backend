from uuid import uuid4
from django.http import request, FileResponse
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
import requests
from datetime import date, datetime
from django.core.files.storage import default_storage
import os
from django.contrib import messages
from django import template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from cubaapp.recognition.tester import identify_face
from django.views.static import serve
from django.db.models import Q




from cubaapp.config import VIOLATIONS_DIRECTORY_PATH, STUDENTS_FOLDER, URL, HAARCASCADES_FOLDER, TRAINING_IMAGES_FOLDER, OUTPUT_FOLDER, BASE_PATH

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)
# Create your views here.

#-------------------------General(Dashboards,Widgets & Layout)---------------------------------------

#---------------Dashboards

@login_required(login_url="/login")
def index(request):
    
    students = Student.objects.all()
    
    
    summary = {
        'installed_cameras': Camera.objects.all().count(),
        'total_images': Images.objects.all().count(),
        'total_reports': Reports.objects.all().count(),
        'total_users': len(students)
        
    }
    context = { "breadcrumb":{"parent":"Dashboard", "child":"Dashboard"}, "summary":summary}
    return render(request,"general/dashboard/default/index.html",context)
    

@login_required(login_url="/login")
def cameras_page(request):
    Cameras_all = Camera.objects.all()
    print(Cameras_all)
    for camera in Cameras_all:
        print("Camera details:")
        for field in camera._meta.fields:
            print(f"{field.name}: {getattr(camera, field.name)}")
        print("\n")
    
    context = {"cameras":Cameras_all, "breadcrumb":{"parent":"Dashboard", "child":"Cameras"}}
    
    return render(request,"cameras/cameras.html",context)

@login_required(login_url="/login")
def delete_camera(request,id):
    print(id)
    selected_camera = Camera.objects.get(camera_ID=id)
    selected_camera.delete()
    url = "/cameras"
    return redirect(url)

    

@login_required(login_url="/login")
def images_page(request):
    
    images = Images.objects.all()

    if request.method == 'POST':
        items = request.POST
        
        start = items.get('start')
        end = items.get('end')
        
        if (start == "" or end == ""):
            messages.warning(request, 'Please select a valid date range')
            images = []
            context = {"images":images,"breadcrumb":{"parent":"Dashboard", "child":"Images"} }    
            return render(request,'images/images.html',context)
        # check if start and end is valid dates
        
        
        images = Images.objects.filter(created__range=[start,end])
        # Check if images is empty
        
        
        print(images)

    for idx in images:
        print(idx.created)
        idx.filename = idx.filename.replace(BASE_PATH,"")
    print(images.__dict__)
    context = {"images":images,"breadcrumb":{"parent":"Dashboard", "child":"Images"} }    
    return render(request,'images/images.html',context)
    

@login_required(login_url="/login")
def camera_create(request):
    
    Cameras_all = Camera.objects.all()
    print(Cameras_all)
    for camera in Cameras_all:
        print("Camera details:")
        for field in camera._meta.fields:
            print(f"{field.name}: {getattr(camera, field.name)}")
        print("\n")
    form = CameraForm()
    
    if request.method == 'POST':
        camera_name = request.POST.get('camera_name')
        ip_address = request.POST.get('ip_address')
        camera_details = request.POST.get('camera_details')
        other_details = request.POST.get('other_details')
        
        Camera.objects.create(camera_name=camera_name,ip_address=ip_address,camera_details=camera_details,other_details=other_details)
        return redirect('/cameras')

    context = {'cameras':Cameras_all, "breadcrumb":{"parent":"Dashboard", "child":"CCTV Create"}}
    return render(request,"cameras/add-camera-page.html",context)


@login_required(login_url="/login")
def add_student_image(request, id):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        
        # Check if folder /static/students/{id} exists
        # If not, create it
        
        student = Student.objects.get(student_ID=id)
        folder_path = os.path.join( BASE_PATH +'static', 'training_images', str(id))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        for file_obj in images:
            # use UUID random string as filename
            filename = str(uuid4()) + os.path.splitext(file_obj.name)[1]
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'wb+') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
                    
                StudentTraniningImage.objects.create(
                    student_ID = student,
                    student_image_filename = filename,
                    student_image_path = file_path
                )
            

        return redirect('/students')

    context = { "breadcrumb":{"parent":"Dashboard", "child":"Add Student Image"}}
        
    
    return render(request,"students/add-image-page.html",context)


@login_required(login_url="/login")
def delete_student(request, id):
    selected_student = Student.objects.get(student_ID=id)

    # Delete the student image
    if selected_student.student_image:
        student_image_path = os.path.join(BASE_PATH+'static/students', selected_student.student_image)
        print(student_image_path)
        if os.path.isfile(student_image_path):
            os.remove(student_image_path)
    
    # Delete the training images for the student
    training_images_path = os.path.join(BASE_PATH + 'static', 'training_images', str(id))
    print(training_images_path)
    if os.path.isdir(training_images_path):
        for file_name in os.listdir(training_images_path):
            file_path = os.path.join(training_images_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(training_images_path)

    # Delete rows from StudentTrainingImage table
    StudentTraniningImage.objects.filter(student_ID=id).delete()

    # Delete the student record
    selected_student.delete()

    return redirect('/students')



@csrf_exempt
@login_required(login_url="/login")
def add_student(request):
    
    if request.method == 'POST':
        required_fields = ['student_name','email','contact','course','section']
        
        if all(field in request.POST and request.POST[field] for field in required_fields):
            student_name = request.POST.get('student_name')
            email = request.POST.get('email')
            contact = request.POST.get('contact')
            course = request.POST.get('course')
            section = request.POST.get('section')
            image = request.FILES.get('image')

            if image is None:
                print("No image")
            else:
                unique_filename = str(uuid4())
                path = os.path.join(STUDENTS_FOLDER, unique_filename + '.jpg')
            
                with open(path, 'wb+') as f:
                        f.write(image.read())
                    
            # save the image on local storage to static/students

            Student.objects.create(student_name=student_name,
                                   student_email=email,
                                   student_contact=contact,
                                   student_course=course,
                                   student_section=section,
                                   student_image = unique_filename + '.jpg'
                                   )
            return redirect('/students')

    context = { "breadcrumb":{"parent":"Dashboard", "child":"Add Student"}}       
    return render(request,"students/add-student-page.html",context)

@login_required(login_url="/login")
def edit_camera(request,id):
    selected_camera = Camera.objects.get(camera_ID=id)
    
    if request.method == 'POST':
        camera = Camera.objects.get(camera_ID=id)
        camera.camera_name = request.POST.get('camera_name')
        camera.camera_IP = request.POST.get('ip_address')
        camera.camera_details = request.POST.get('camera_details')
        camera.other_details = request.POST.get('other_details')
        
        camera.save()
        return redirect('/cameras')
            
    
    context = {"camera":selected_camera, "breadcrumb":{"parent":"Dashboard", "child":"Edit Camera"}}
    return render(request,"cameras/edit-camera-page.html",context)


@login_required(login_url="/login")
def reports(request):
    
    
    if request.method == 'POST' and request.POST.get('search_date'):
        search_date = request.POST.get('search_date')
        
        reports_all = Reports.objects.filter(report_date__date=search_date)
        # Check if images is empty
    else:
        reports_all = Reports.objects.all()
        
        
    
    context = { "breadcrumb":{"parent":"Dashboard", "child":"Reports"},  "reports":reports_all}
    return render(request,"reports/reports-page.html",context)
    


@login_required(login_url="/login")
def students(request):

    all_students = Student.objects.all()
    print(all_students)

    context = { "breadcrumb":{"parent":"Dashboard", "child":"Students"}, "students":all_students}
    return render(request,"students/students.html",context)


@login_required(login_url="/login")
def edit_student(request, id):
    
    if request.method == 'POST':
        required_fields = ['student_name','email','contact','course','section']
        
        if all(field in request.POST and request.POST[field] for field in required_fields):
            
            student = Student.objects.get(student_ID=id)
            student.student_name = request.POST.get('student_name')
            student.student_email = request.POST.get('email')
            student.student_contact = request.POST.get('contact')
            student.student_course = request.POST.get('course')
            student.student_section = request.POST.get('section')
            
            if request.FILES.get("image"):
                unique_filename = str(uuid4())
                path = os.path.join(STUDENTS_FOLDER, unique_filename + '.jpg')
                
                
            
                student.student_image = request.FILES.get("image")
            
            
            student.save()
            
            return redirect('/students')
        # Check first if POST form is complete
    
    # Get student details'

    selected_student = Student.objects.get(student_ID=id)

    context = { "breadcrumb":{"parent":"Dashboard", "child":"Edit Student"}, "student":selected_student}
    
    return render(request,"students/edit-student-page.html",context)
    
    

@login_required(login_url="/login")
def about(request):
    context = { "breadcrumb":{"parent":"Dashboard", "child":"About"}}
    return render(request,"about/about-page.html",context)

#---------------------------------user
@login_required(login_url="/login")
def user_profile(request):
    context = { "breadcrumb":{"parent":"Users", "child":"User Profile"}}
    return render(request,"applications/user/user-profile/user-profile.html",context)
    

@login_required(login_url="/login")
def recognize(request, id):
    source_image = Images.objects.get(id=id)
    # print(source_image.filename)
    # file = open(source_image.filename, 'rb')
    # response = requests.post('http://localhost:5000/recognize', files={'image': file})
    # print(response)    
    
    response ={
        'output': {'label': 2,
                   'url': 'http://localhost:5000/static/get_output/10605.jpg'
                   },
        'student': {'contact': '09213123',
                    'course': 'College of Engineering',
                    'date_created': 'Tue, 21 Feb 2023 05:29:01 GMT',
                    'email': 'bezos@email.com',
                    'id': 2, 'name': 'Jeff Bezos',
                    'section': 'Amazon'
                    },
        'success': 'Image recognized successfully!'
        }
    
    original_image = source_image
    student = response['student']
    results = response['output']
    context = { "breadcrumb":{"parent":"Users", "child":"Recognize"}, "results":results , "student":student, "original_image":original_image}
    return render(request, "images/recognize/recognize.html", context)

@login_required(login_url="/login")
def user_cards(request):
    users = User.objects.all()
    
    print(users)
    
    context = {"users":users, "breadcrumb":{"parent":"Users", "child":"User Cards"}}
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


@login_required(login_url="/login")
def generate_report(request):
    url = 'fmthesis.pythonanywhere.com'
    students_list = Student.objects.all()
        
    generate_date_str = request.POST.get('generate_date', date.today())
    if generate_date_str == '':
        messages.warning(request, 'Please select a valid date.')
        return redirect('reports')
    selected_date = datetime.strptime(generate_date_str, '%Y-%m-%d').date()
    new_report = Reports.objects.create(
        report_date = selected_date
    )
    
    found_images = Images.objects.filter(created__date=selected_date)
    # Redirect to the report page if no images found
    
    if found_images.count() == 0:
        # Create an email and pdf report that no images were found
        messages.warning(request, 'No images found for the selected date.')
        return redirect('reports')
    
    student_obj = {}
    for student in students_list:
        student_obj[int(student.student_ID)] = student.student_name
    
    # filenames = found_images.values_list('filename', flat=True)
    
    matched_count = 0
    unknown_count = 0
    for file in found_images:
        file_path = os.path.join(VIOLATIONS_DIRECTORY_PATH, file.filename)
        output_filename,label =identify_face(file_path,student_obj)
        print(serve_violations_image(request, file.id))
        if label == 'Unknown':
            unknown_count = unknown_count + 1
            matched_student = None
        else:
            matched_student = ''
            matched_count = matched_count + 1
            for key, value in student_obj.items():
                print(key, value)
                if key == label:
                    print(f'The key associated with value {output_filename} is {key}')
                    matched_student = Student.objects.get(student_ID=key)
                    break
        
        ImageOutputImage.objects.create(
            report_ID = new_report,
            image_output_filename = output_filename,
            source_image_filename = file.filename,
            student = matched_student,
            image =file
        )
            
    pdf = fetch_pdf_template(new_report.report_ID)
    
    new_report.output_url = pdf['download_url']
    new_report.unknown_faces_count = unknown_count
    new_report.report_source_images_matched_count = matched_count
    
    new_report.save()
    
    if matched_count == 0:
        message = f"No matches found for the selected date ({selected_date})."
    else:
        message = f"Report generated successfully. <br><br><b>Report Date: </b>{selected_date}<br><b>Source Images Count: </b>{ matched_count + unknown_count}<br><b>Matched Images Count: </b>{matched_count}<br><b>Unknown Faces Count: </b>{unknown_count}<br><br>To view the full report in HTML, click <a href='{url}'>here</a>.<br>To download the full report in PDF, click <a href='{pdf['download_url']}'>here</a>."


    # Send email
    
    # Get all Users 
    all_user = User.objects.all()
    email_list = []
    for user in all_user:
        email_list.append(user.userid.email)
        
    
    
    send_email(subject="Facemask Detection System",
           message=message,
           from_email="fm.thesis2023@gmail.com",
           to_email=email_list,
           smtp_username="fm.thesis2023@gmail.com",
           smtp_password="hkcsjzeonfntkbzv",
           cc_email = 'fm.thesis2023@gmail.com',
           )
    return redirect('reports')
    

#---------------------------------------------------------------------------------------
@login_required(login_url="/login")
def reports_view(request,id):
    report = Reports.objects.get(report_ID=id)
    output_images = ImageOutputImage.objects.filter(report_ID=report)
    print(output_images.__dict__)
    
    
    context = {"breadcrumb":{"parent":"Reports", "child":"View Report"}, "report":report, 'details':output_images}
    
    return render(request,'reports/reports-view.html',context)

@login_required(login_url="/login")
def delete_report(request, id):
    report = Reports.objects.get(report_ID=str(id))
    report.delete()
    return redirect('/reports')
    


@login_required(login_url="/login")
def edit_profile(request):
    form = UserForm()
    # clean up for the database incase of errors
    # User.objects.all().delete()
    user = request.user
    
    all_user = User.objects.all()

    for item in all_user:
        print(item.userid.email)
    
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
    filename = req.get('filename')
    path = os.path.join(VIOLATIONS_DIRECTORY_PATH, filename)
    ip_address = req.get('ip_address')
    
    try:
        camera = Camera.objects.get(ip_address=ip_address)
    except Exception as e:
        return HttpResponse("Camera not found {0}".format(e), status = 400)

    
    
    
    with open(path, 'wb') as f:
        f.write(imgdata)

    Images.objects.create(filename=filename, path=path,source_id=camera, source_ip_address=ip_address) 
    
    return HttpResponse("return this string")


@login_required(login_url="/login")
def delete_image(request, pk):
    if request.method == "POST":
        image = Images.objects.get(id=pk)
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
                next_page = request.GET['next']
                print(next_page)
                return HttpResponseRedirect(next_page)
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

    


def send_email(subject, message, from_email, to_email, image_path=None, smtp_server='smtp.gmail.com', smtp_port=587, smtp_username=None, smtp_password=None, cc_email=None):
    # Create a message object
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['Subject'] = subject
    
    msg["To"] = ','.join(to_email)

    # Add CC recipients to the message object, if provided
    # Attach the message to the message object
    msg.attach(MIMEText(message, 'html'))

    # Attach the image to the message object, if provideds
    if image_path:
        with open(image_path, 'rb') as f:
            img_data = f.read()
        image = MIMEImage(img_data, name='image.png')
        msg.attach(image)

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Send the email and close the connection
    recipients = ','.join(to_email)
    print(recipients, msg["To"])
    for email in to_email:
        print(email)
        server.sendmail(from_email, email, msg.as_string())
    server.quit()
    

def serve_violations_image(request, id):
    directory = BASE_PATH + 'static/assets/violations' # Replace with the actual path to your directory
    image = Images.objects.get(id=id)
    return serve(request, image.filename, directory)


def serve_output_image(request, id):
    directory = BASE_PATH + 'cubaapp/static/output' # Replace with the actual path to your directory
    image = ImageOutputImage.objects.get(image_output_image_ID=id)
    return serve(request, image.image_output_filename, directory)


def fetch_pdf_template(id):
    
    report = Reports.objects.get(report_ID=id)
    print(report)
    
    
    all_camera = Camera.objects.all()
    camera_arr = []
    
    for camera in all_camera:
        
        cameras = Camera.objects.filter(
            Q(date_created__exact=report.report_date)
        )
        
        camera_arr.append({
            "camera_name": camera.camera_name,
            "ip_address": camera.ip_address,
            "location":camera.camera_details,
            "image_found_today": len(cameras),
        })
    
    recognition_results = []
    output_images = ImageOutputImage.objects.filter(report_ID = report)
    
   
    for output_image in output_images:
        
        recognition_results.append({
            "source_image_url":URL + "serve_violations_image/" + str(output_image.image.id),
            "output_image_url":URL + "serve_output_image/" + str(output_image.image_output_image_ID),
            "student_details":{
                "name":output_image.student.student_name if output_image.student else 'NONE',
                "email":output_image.student.student_email if output_image.student else 'NONE'                      ,
                "contact_number":output_image.student.student_contact if output_image.student else 'NONE',
                "course":output_image.student.student_course if output_image.student else 'NONE',  
                "section":output_image.student.student_section if output_image.student else 'NONE',
            },
            "image_details":{
                "datetime_created": output_image.image.created.strftime('%Y-%m-%d %H:%M:%S'),
                "source_camera":{
                    "camera_name":output_image.image.source_id.camera_name,
                    "camera_details":output_image.image.source_id.camera_details,
                    "other_details":output_image.image.source_id.other_details,
                    "ip_address":output_image.image.source_id.ip_address
                }

            }
        })
    
    
    
    pdf_object = {
        "batchNumber": "736628",
        "revision": "0",
        "header_title": "Facemask Detection System",
        "website": "https://fmthesis.pythonanywhere.com/",
        "document_id": "889856789012",
        "camera": camera_arr,
        "recognition_results":recognition_results
    }
    
    json_data = json.dumps(pdf_object)  # convert dictionary to JSON string
    
    
    api_key = '9cf6MTEzMjM6ODM2OTp3SklzR3hYVkVqYklXaVd'
    template_id = '72477b238436780c'
    
    response = requests.post(
        F"https://rest.apitemplate.io/v2/create-pdf?template_id={template_id}",
        headers = {"X-API-KEY": F"{api_key}"},
        json= pdf_object
    )
    print(response.content)
    
    return response.json()
    
    