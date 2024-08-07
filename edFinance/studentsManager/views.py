import pandas as pd
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from .models import Student
from .forms import UploadFileForm
from datetime import datetime
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
    total_students = students.count()
    context = {'students': students,'totalStudents':total_students}
    return render(request, 'studentsManager/students.html', context )


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)

            # Extract data from the Excel file
            data = pd.read_excel(file_path)
            for index, row in data.iterrows():
                dob = datetime.strptime(row['Data of Birth'], '%d-%m-%Y').date() if pd.notnull(row['Data of Birth']) else None
                gender = 'M' if row['Gender'] == 'Male' else 'F' if row['Gender'] == 'Female' else 'O'

                Student.objects.create(
                    student_name=row['Name'],
                    gender=gender,
                    student_class=row['Class'],
                    parents_phone_number=row['Phone Number'] if pd.notnull(row['Phone Number']) else None,
                    dob=dob,
                    school=request.user,  # Assuming the logged-in user is the school
                )

            # Delete the file after processing
            fs.delete(filename)

            return redirect('success')  # Redirect to a success page or another view
    else:
        form = UploadFileForm()
    return render(request, 'studentsManager/upload.html', {'form': form})


def successMessgae(request):
    return render(request,'studentsManager/success.html')