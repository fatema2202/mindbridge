from django.contrib import admin
from .models import Therapist, Appointment, CommunityForum, ProgressJournal, Payment, UserProfile, Testimonial

admin.site.register(Therapist)
admin.site.register(Appointment)
admin.site.register(CommunityForum)
admin.site.register(ProgressJournal)
admin.site.register(Payment)
admin.site.register(UserProfile)
admin.site.register(Testimonial)