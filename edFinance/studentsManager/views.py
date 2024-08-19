from django.http import HttpResponse
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
from .forms import editStudentForm
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

@login_required
def editStudent(request,StudentId):
    studentInfo = Student.objects.get(id_no=StudentId)
    form = editStudentForm(instance=studentInfo)
    if str(request.user) != str(studentInfo.school_username):
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        studentInfo.student_name = request.POST.get("student_name")
        studentInfo.gender = request.POST.get("gender")
        studentInfo.student_class = request.POST.get("student_class")
        studentInfo.parents_phone_number = request.POST.get("parents_phone_number")
        studentInfo.dob = request.POST.get("dob")
        studentInfo.save()
        return redirect('students')

    context = {'form': form,'student':studentInfo}
    return render(request, 'studentsManager/editStudentInfo.html', context)

@login_required
def deleteStudent(request,StudentId):
    studentInfo = Student.objects.get(id_no=StudentId)
    if str(request.user) != str(studentInfo.school_username):
        return HttpResponse('Your are not allowed here!!')
    studentInfo.delete()
    return redirect("students")

@login_required
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

@login_required
def successMessgae(request):
    return render(request,'studentsManager/success.html')

def download_sample_excel(request):
    # Define the path to the Excel file
    file_path = os.path.join(settings.BASE_DIR, 'studentsManager', 'files', 'sample.xlsx')

    # Open the file and read its content
    with open(file_path, 'rb') as f:
        file_data = f.read()

    # Create the HTTP response
    response = HttpResponse(file_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="sample_excel.xlsx"'

    return response
