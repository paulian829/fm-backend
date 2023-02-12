# from django.conf.urls import url
from django.urls import path
from . import views
from django.urls import path
from . import views


urlpatterns = [

path('cameras', views.cameras_page, name="dashboard_02"),

path('images', views.images_page, name="general_widget"),
path('camera_create', views.camera_create, name="cctv_create"),
path('delete_camera/<str:id>', views.delete_camera, name="delete_camera"),
path('edit_camera/<str:id>', views.edit_camera, name="edit_camera"),
path('reports', views.reports, name="chart_widget"),

path('settings', views.projects, name="projects"),
path('about', views.project_create, name="projectcreate"), 

path('edit_profile', views.edit_profile, name="edit_profile"),
path('user_cards', views.user_cards, name="user_cards"),


path('form_validation', views.form_validation, name="form_validation"),
path('base_input', views.base_input, name="base_input"),

path('lists', views.lists, name="lists"),

path('buttons/', views.buttons, name="buttons"),

path('reset_password', views.reset_password, name="reset_password"),

path('gallery_grid', views.gallery_grid, name="gallery_grid"),
path('grid_description', views.grid_description, name="grid_description"),

path('FAQ', views.FAQ, name="FAQ"),
path('delete_image/<str:pk>', views.delete_image, name="delete_image"),
# path('to_do', views.to_do, name="to_do"),
# path('delete/<str:pk>/', views.deleteTask, name="delete"),
# path('updateTask/<str:pk>/', views.updateTask,name='updateTask'),
# path('markAllComplete/', views.markAllComplete, name='markAllComplete'),
# path('markAllIncomplete/', views.markAllIncomplete, name='markAllIncomplete'),
path('add_image/',views.add_image, name='add_image'),

path('logout', views.logout_view, name="logout_view"),
path('index', views.index, name="index"),
path('login', views.login_simple, name="login"),
path('register_simple', views.register_simple, name="register_simple"),
path('', views.login_simple, name="login_simple"),
    



]