"""
URL configuration for projekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/<int:user_id>/', views.home_view, name='home'),
    path('studlist/', views.stud_list, name='studlist'),
    path('proflist/', views.prof_list, name='proflist'),
    path('logout/', views.logout_view, name='logout'),
    path('addsubj/', views.add_subj, name='addsubj'),
    path('subjlist/', views.subj_list, name='subj_list'),
    path('subjlist/edit/<int:subject_id>/', views.editsubj, name='edit_subj'),
    path('addstud/', views.add_stud, name='addstud'),
    path('studlist/edit/<int:user_id>/', views.editstud, name='edit_stud'),
    path('addprof/', views.add_prof, name='addprof'),
    path('proflist/edit/<int:user_id>/', views.editprof, name='edit_prof'),
    path('student/<int:user_id>/', views.stud_details, name='stud_details'),
    path('profesor/<int:user_id>/', views.prof_details, name='prof_details'),
    path('subject/<int:subject_id>/', views.subj_details, name='subj_details'),
    path('upisni_list/', views.enrollment_list, name='upisni_list'),
    path('enroll_in_subj/', views.enroll_in_subject, name='enroll_in_subject'),
    path('enrollment_list/<int:student_id>/', views.enrollment_list, name='enrollment_list'),
    path('enrollment/delete/<int:enrollment_id>/', views.delete_enrollment, name='delete_enrollment'),
    path('enr_stud/<int:subject_id>/', views.enrolled_students, name='enr_stud'),
    path('prof_subj/', views.prof_subj, name='prof_subj'),
    path('subjects/<int:subject_id>/students/', views.enrolled_students, name='enr_stud'),
    path('student/<int:student_id>/enrollments/', views.enrollment_list, name='enrollment_list'),
    path('student/<int:student_id>/enrollments/add/', views.add_enrollment, name='add_enrollment'),
    path('enrollment/<int:enrollment_id>/update/', views.update_enrollment, name='update_enrollment'),
    path('enrollment/<int:enrollment_id>/delete/', views.delete_enrollment, name='delete_enrollment'),
    path('stud_30/', views.stud_30, name='stud_30'),
]