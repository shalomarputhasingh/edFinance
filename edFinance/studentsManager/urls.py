from django.urls import path
from . import views
urlpatterns = [
    path('students/', views.student_list,name="students"),
    path('addStudent/',views.add_student,name="addStudent"),
]