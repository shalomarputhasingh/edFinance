from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student

@login_required
def add_student(request):
    if request.method == 'POST':
        student_name = request.POST['student_name']
        gender = request.POST['gender']
        student_class = request.POST['student_class']
        parents_phone_number = request.POST['parents_phone_number']
        dob = request.POST['dob']

        student = Student(
            student_name=student_name,
            gender=gender,
            student_class=student_class,
            parents_phone_number=parents_phone_number,
            dob=dob,
            school=request.user  # Link to the logged-in user
        )
        student.save()
        return redirect('students')

    return render(request, 'studentsManager/student_form.html')

@login_required
def student_list(request):
    students = Student.objects.filter(school=request.user)
    return render(request, 'studentsManager/students.html', {'students': students})
