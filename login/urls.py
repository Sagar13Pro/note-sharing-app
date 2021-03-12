from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # views
    path('', views.SignIn, name="login"),
    path('user/registration/', views.SignUp, name="registration"),
    path('user/create_note', views.Notes, name="note_view"),
    path('user/myvault/', views.Dashboard, name="user_dashboard"),
    path('user/dashboard/search_result' , views.search_Result , name ="search_Result"), 
    path('user/dashboard/search' , views.search_Result , name ="search_Result_search"), 
    path('user/note/edit/<int:id>',views.Edit, name="note_edit"),
    path('user/note/share/<int:id>',views.Share, name="note_share"),
    path('user/note/shared/view/<int:id>',views.SharedView, name="note_shared_view"),
   
    # Controllers
    path('registration/save/user/', views.Save, name="user_save"),
    path('user/login/', views.ValidateUser, name="user_login"),
    path('user/create_note/store', views.create_note, name="note_save"),
    path('user/logout/', views.Logout, name="user_logout"),
    path('user/note/edit/<int:id>/store', views.EditStore, name="note_edit_store"),
    path('user/note/shared/<int:id>/',views.ShareNote, name="note_share_to"),

    #for password checking note shared to user
    #path('user/note/shared/<int:id>',views.SharedViewMatch, name="note_shared_match"),
    path('user/note/<int:id>/delete',views.Delete,name="note_delete"),
    path('password_reset/' , views.fg_pass , name="password_reset"),
    path('password_reset/reset_password' , views.validate_password , name ="rest_password"),
    path('user/reset_password/<int:id>' , views.resest_password , name="Reset_Password"),
    path('user/reset_password/Password_Reset',views.reset_done , name="reset-done")
]
  