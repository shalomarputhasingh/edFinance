from django.urls import path
from . import views
urlpatterns = [
    path("createStudentFees/<str:pk>",views.createFees, name="addFees"),
    path("fees/",views.feesLister,name="fees"),
    path("feesDetails/<str:pk>",views.studentFeeDetails,name="feeDetails"),
    path("billingDetails/<str:pk>",views.studentBillingFees,name="billingDetails"),
]