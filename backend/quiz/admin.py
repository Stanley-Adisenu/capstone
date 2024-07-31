from django.contrib import admin
from .models import Questions,Quiz,QuizAttempt,Department,Level,Course,Choice

# Register your models here.
admin.site.register(QuizAttempt)
admin.site.register(Quiz)
admin.site.register(Questions)
admin.site.register(Department)
admin.site.register(Level)
admin.site.register(Course)
admin.site.register(Choice)
