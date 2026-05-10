import site

from django.contrib import admin
from .models import Doctor, Patient , PatientHistory, Review,ReviewRequest
# Register your models here
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(PatientHistory)
admin.site.register(Review)
admin.site.register(ReviewRequest) 