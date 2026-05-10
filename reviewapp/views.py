from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .models import *


def login_page(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # =========================
            # ADMIN LOGIN
            # =========================

            if user.is_superuser:

                return redirect('dashboard')

            # =========================
            # DOCTOR LOGIN
            # =========================

            elif Doctor.objects.filter(user=user).exists():

                doctor = Doctor.objects.get(user=user)
                return redirect('doctor_dashboard', doctor_id=doctor.id)

            # =========================
            # PATIENT LOGIN
            # =========================

            elif Patient.objects.filter(user=user).exists():

                return redirect('patient_dashboard')

            else:

                messages.error(request,
                'No Role Assigned')

                return redirect('login')

        else:

            messages.error(request,
            'Invalid Username or Password')

            return redirect('login')

    return render(request, 'login.html')
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def dashboard(request):
    dc = Doctor.objects.count()
    pc = Patient.objects.count()
    rc= Review.objects.count()
    doctors = Doctor.objects.all().order_by('-id')
    return render(request, 'dashboard.html', {'doctors': doctors, 'dc': dc, 'pc': pc, 'rc': rc})
@login_required
def view_doctors(request):
    doctors = Doctor.objects.all().order_by('-id')
    return render(request, 'view_doctors.html', {'doctors': doctors})
@login_required
def view_patients(request):
    patients = Patient.objects.all().order_by('-id')
    return render(request, 'view_patients.html', {'patients': patients})
@login_required
def view_reviews(request):
    reviews = Review.objects.all().order_by('-id')
    return render(request, 'view_reviews.html', {'reviews': reviews})
@login_required
def add_doctor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        address = request.POST.get('address')
        username = email

        password = 'doctor123'

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Doctor.objects.create(

            user=user,

            name=name,
            email=email,
            phone=phone,

            department=department,

            qualification=qualification,

            experience=experience,

            address=address,
        )

        messages.success(request, 'Doctor Added Successfully')

        return redirect('view_doctors')

    return render(request, 'add_doctor.html')

@login_required
def add_patient(request):
    doctors = Doctor.objects.all()
    if request.method == 'POST':

        name = request.POST.get('name')

        age = request.POST.get('age')

        gender = request.POST.get('gender')

        phone = request.POST.get('phone')

        email = request.POST.get('email')

        blood_group = request.POST.get('blood_group')

        disease = request.POST.get('disease')

        address = request.POST.get('address')

        doctor_id = request.POST.get('doctor')

        doctor = Doctor.objects.get(id=doctor_id)

        username = email

        password = 'patient123'

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Patient.objects.create(

            user=user,

            doctor=doctor,

            name=name,

            age=age,

            gender=gender,

            email=email,

            phone=phone,

            blood_group=blood_group,

            disease=disease,

            address=address,

        )
        messages.success(request, 'Patient Added Successfully')

        return redirect('view_patients')
    return render(request, 'add_patient.html', {'doctors': doctors})
@login_required
def doctor_dashboard(request, doctor_id):

    doctor = Doctor.objects.get(id=doctor_id)

    patients = Patient.objects.filter(
        doctor=doctor
    ).order_by('-id')

    context = {

        'doctor': doctor,

        'patients': patients

    }

    return render(
        request,
        'doctor_dashboard.html',
        context
    )
@login_required
def patient_details(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    history = PatientHistory.objects.filter(patient=patient).order_by('-id')
    return render(request, 'patient_details.html', {'patient': patient, 'history': history})
@login_required
def add_medical_history(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    doctor = Doctor.objects.get(
        user=request.user
    )

    if request.method == 'POST':

        diagnosis = request.POST.get('diagnosis')

        prescription = request.POST.get('prescription')

        treatment = request.POST.get('treatment')

        visit_date = request.POST.get('visit_date')

        next_visit_date = request.POST.get(
            'next_visit_date'
        )

        notes = request.POST.get('notes')

        PatientHistory.objects.create(

            patient=patient,

            doctor=doctor,

            diagnosis=diagnosis,

            prescription=prescription,

            treatment=treatment,

            visit_date=visit_date,

            next_visit_date=next_visit_date,

            notes=notes

        )

        messages.success(
            request,
            'Medical History Added Successfully'
        )

        return redirect(
            'patient_details',
            patient_id=patient.id
        )

    context = {

        'patient': patient

    }

    return render(
        request,
        'add_medical_history.html',
        context
    )
@login_required
def patient_dashboard(request):
    patient = Patient.objects.get(user=request.user)
    history = PatientHistory.objects.filter(patient=patient).order_by('-id')
    review = Review.objects.filter(patient=patient).order_by('-id')
    return render(request, 'patient_dashboard.html', {'patient': patient, 'history': history,'reviews': review})
@login_required
@login_required(login_url='login')
def add_review(request):

    patient = Patient.objects.get(
        user=request.user
    )

    doctor = patient.doctor

    if request.method == 'POST':

        rating = request.POST.get('rating')

        review = request.POST.get('review')

        Review.objects.create(

            patient=patient,

            doctor=doctor,

            rating=rating,

            review=review

        )

        messages.success(
            request,
            'Review Submitted Successfully'
        )

        return redirect('patient_dashboard')

    context = {

        'patient': patient,

        'doctor': doctor

    }

    return render(
        request,
        'add_review.html',
        context
    )