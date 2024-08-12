from django.urls import path
from . import views
urlpatterns = [
    path("createStudentFees/<str:pk>",views.createFees, name="addFees")
]