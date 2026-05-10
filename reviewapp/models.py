from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Doctor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    department = models.CharField(max_length=100)

    qualification = models.CharField(max_length=200)

    experience = models.PositiveIntegerField()

    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Patient(models.Model):

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    BLOOD_GROUPS = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=200)

    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES
    )

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    blood_group = models.CharField(
        max_length=10,
        choices=BLOOD_GROUPS
    )

    disease = models.CharField(max_length=200)

    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class PatientHistory(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='history'
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True
    )

    diagnosis = models.TextField()

    prescription = models.TextField()

    treatment = models.TextField()

    visit_date = models.DateField()

    next_visit_date = models.DateField(
        blank=True,
        null=True
    )

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.visit_date}"
class Review(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    rating = models.PositiveIntegerField()

    review = models.TextField()

    is_submitted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} Review"


# =========================
# REVIEW EMAIL TRACK MODEL
# =========================

class ReviewRequest(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    email = models.EmailField()

    token = models.CharField(max_length=200)

    is_reviewed = models.BooleanField(default=False)

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email