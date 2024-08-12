from django.shortcuts import render

# Create your views here.
def createFees(request,pk):
    context = {'student':pk}
    return render(request, 'billsManager/createFees.html', context)