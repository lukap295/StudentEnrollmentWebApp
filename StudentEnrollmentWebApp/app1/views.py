from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, PredmetiForm, StudentForm, ProfesorForm, EnrollmentForm
from .models import User, Predmeti, Enrollment
from django.http import HttpResponseRedirect

#povezati nekako registraciju, modele na ovaj register_view za različite role


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            role = form.cleaned_data.get('role')
            status = form.cleaned_data.get('status')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  #Redirect to login page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect(f'/home/{user.id}')  # Redirect to the home page with user id
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

@login_required
def home_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.id != user.id:
        return redirect('home', user_id=request.user.id)
    return render(request, 'home.html', {'user': user})

def logout_view(request):
    logout(request)
    return redirect('index')

def index_view(request):
    return render(request, "index.html", {"hello": "Hello"})

def stud_list(request):
    User = get_user_model()
    users = User.objects.filter(role='stu')
    return render(request, "studlist.html", {"users" : users})

def prof_list(request):
    User = get_user_model()
    users = User.objects.filter(role='prof')
    return render(request, "proflist.html", {"users" : users})

def subj_list(request):
    subjects = Predmeti.objects.all()
    return render(request, "subjlist.html", {"subjects": subjects})

@login_required
def add_subj(request):
    user_id = request.user.id
    role = str(request.user.role)
    if role != 'admin':
        return redirect(f'/home/{user_id}')
    
    if request.method == 'POST':
        form = PredmetiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/home/{user_id}')
    else:
        form = PredmetiForm()
    
    return render(request, 'addsubj.html', {'form': form})

@login_required
def editsubj(request, subject_id):
    subject = get_object_or_404(Predmeti, id=subject_id)
    role = str(request.user.role)
    if role != 'admin':
        return redirect('/subjlist')

    if request.method == "POST":
        form = PredmetiForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subj_list')  # Redirect to the list of subjects after saving
    else:
        form = PredmetiForm(instance=subject)

    return render(request, 'editsubj.html', {'form': form, 'subject': subject})

@login_required
def subj_details(request, subject_id):
    subject = get_object_or_404(Predmeti, id=subject_id)
    return render(request, 'subj_det.html', {'subject': subject})

@login_required
def add_stud(request):
    user_id = request.user.id
    role = str(request.user.role)
    if role != 'admin':
        return redirect(f'/home/{user_id}')
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/home/{user_id}')  # Redirect after successful form submission
    else:
        form = StudentForm()
    
    return render(request, 'addstud.html', {'form': form})

@login_required
def editstud(request, user_id):
    student = get_object_or_404(User, id=user_id)
    role = str(request.user.role)
    if role != 'admin':
        return redirect('/studlist')
    
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('studlist')
    else:
        form = StudentForm(instance=student)

    return render(request, 'editstud.html', {'form': form, 'student': student})

@login_required
def stud_details(request, user_id):
    student = get_object_or_404(User, id=user_id)
    return render(request, 'stud_det.html', {'student': student})

@login_required
def add_prof(request):
    user_id = request.user.id
    role = str(request.user.role)
    if role != 'admin':
        return redirect(f'/home/{user_id}')
    
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/home/{user_id}')
    else:
        form = ProfesorForm()
    
    return render(request, 'addprof.html', {'form': form})

@login_required
def editprof(request, user_id):
    profesor = get_object_or_404(User, id=user_id)
    role = str(request.user.role)
    if role != 'admin':
        return redirect('/proflist')
    if request.method == "POST":
        form = ProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            return redirect('proflist')
    else:
        form = ProfesorForm(instance=profesor)

    return render(request, 'editprof.html', {'form': form, 'profesor': profesor})

@login_required
def prof_details(request, user_id):
    profesor = get_object_or_404(User, id=user_id)
    subjects = Predmeti.objects.filter(nositelj=profesor)
    return render(request, 'prof_det.html', {'profesor': profesor, 'subjects' : subjects})

@login_required
def enrollment_list(request, student_id):
    student = get_object_or_404(User, id=student_id)
    enrollments = Enrollment.objects.filter(student=student)
    return render(request, 'upisni_list.html', {'enrollments': enrollments, 'student': student})

def enroll_in_subject(request):
    user_id = request.user.id
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, user=request.user)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = request.user
            enrollment.save()
            return redirect(f'/home/{user_id}')
    else:
        form = EnrollmentForm(user=request.user)
    return render(request, 'enroll_in_subj.html', {'form': form, 'user_id': user_id})

@login_required
def edit_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('upisni_list')
    else:
        form = EnrollmentForm(instance=enrollment, user=request.user)
    return render(request, 'edit_upisni.html', {'form': form, 'enrollment': enrollment})

@login_required
def delete_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    student_id = enrollment.student.id
    if enrollment.student == request.user or request.user.role == 'admin':
        enrollment.delete()
        return redirect('enrollment_list', student_id=student_id)
    else:
        return HttpResponseRedirect('/home/')
    
def enrolled_students(request, subject_id):
    subject = get_object_or_404(Predmeti, id=subject_id)
    status_filter = request.GET.get('status_filter', '')

    if status_filter:
        enrollments = Enrollment.objects.filter(subject=subject, status=status_filter)
    else:
        enrollments = Enrollment.objects.filter(subject=subject)

    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')
        status = request.POST.get('status')
        enrollment = get_object_or_404(Enrollment, id=enrollment_id)
        enrollment.status = status
        enrollment.save()
        return redirect('enr_stud', subject_id=subject_id)

    return render(request, 'enr_stud.html', {
        'subject': subject,
        'enrollments': enrollments
    })


@login_required
def enrollment_list(request, student_id):
    student = get_object_or_404(User, id=student_id)
    enrollments = Enrollment.objects.filter(student=student).order_by('subject__sem_red')
    subjects = Predmeti.objects.all()
    return render(request, 'upisni_list.html', {
        'student': student,
        'enrollments': enrollments,
        'subjects': subjects,
    })

@login_required
def add_enrollment(request, student_id):
    student = get_object_or_404(User, id=student_id)
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        subject = get_object_or_404(Predmeti, id=subject_id)
        if Enrollment.objects.filter(student=student, subject=subject).exists():
            messages.error(request, f"{student.username} is already enrolled in {subject.Ime}.")
        else:
            Enrollment.objects.create(student=student, subject=subject)
            messages.success(request, f"{subject.Ime} has been successfully added for {student.username}.")
        return redirect('enrollment_list', student_id=student_id)
    return redirect('enrollment_list', student_id=student_id)

@login_required
def update_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        enrollment.status = status
        enrollment.save()
        return redirect('enrollment_list', student_id=enrollment.student.id)
    return redirect('enrollment_list', student_id=enrollment.student.id)

def prof_subj(request):
    if request.user.role != 'prof':
        return redirect('home', user_id=request.user.id)

    subjects = Predmeti.objects.filter(nositelj=request.user)
    return render(request, 'prof_subj.html', {'subjects': subjects})

@login_required
def stud_30(request):
    enrollments = Enrollment.objects.select_related('student', 'subject')
    #spremi u rjecink
    student_ects = {}

    for enrollment in enrollments:
        student = enrollment.student
        subject_ects = enrollment.subject.ECTS

        if student not in student_ects:
            student_ects[student] = 0
        student_ects[student] += subject_ects
    stud_30 = [
        (student, total_ects) for student, total_ects in student_ects.items() if total_ects >= 30
    ]

    context = {
        'stud_30': stud_30,
    }
    return render(request, 'stud_30.html', context)

#ponavljaju se predmeti u upisnom listu, to triba prominiti