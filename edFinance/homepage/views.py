from django.shortcuts import redirect, render

# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 
    return render(request, 'homepage/home.html')