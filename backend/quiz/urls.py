from django.urls import path
from . import views 

urlpatterns = [
   path('departments/',views.department_list),
   path('courses/',views.course_list),
   path('quiz/',views.quiz_list),
   path('quiz/<int:pk>/',views.quiz_list_detail),
   path('attempts/',views.quiz_attempt),
   path('attempts/<int:pk>/',views.quiz_attempt_detail),
   path('startquiz/',views.create_quiz_attempt),
   path('leaderboard/',views.leaderboard_view),
   path('home/',views.home),

]
