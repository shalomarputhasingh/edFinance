from django.http import HttpResponse
from django.shortcuts import redirect, render
from billsManager.models import Fee
from studentsManager.models import Student
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import get_object_or_404
@login_required
def createFees(request, pk):
    studentInfo = get_object_or_404(Student, id_no=pk)  # Fetch the Student or return a 404 if not found

    if request.method == 'POST':
        amountEntered = request.POST.get("fees-amount")
        dueDateEntered = request.POST.get("due-date")
        
        # Check if the required fields are present
        if not amountEntered or not dueDateEntered:
            return render(request, 'billsManager/createFees.html', {
                'student': studentInfo,
                'error': 'All fields are required.'
            })
        
        # Try to create and save the Fee instance
        try:
            fee = Fee(
                student=studentInfo,  # Link the Student object directly
                amount=amountEntered,
                due_date=dueDateEntered,
                status='pending'
            )
            fee.save()  # Save the Fee instance to the database
            
            studentInfo.student_fees = True
            studentInfo.save()  # Save the updated Student instance
            
            return redirect('students')  # Redirect to the students page after successful creation

        except Exception as e:
            # Log the exception or print it out for debugging
            print(f"Error saving fee: {e}")
            return render(request, 'billsManager/createFees.html', {
                'student': studentInfo,
                'error': 'There was an error processing your request. Please try again.'
            })
    
    # Render the form if the request method is GET
    if studentInfo.student_fees == False:
        return render(request, 'billsManager/createFees.html', {'student': studentInfo})
    else:
        return redirect('students')
    
@login_required
def feesLister(request):
    students = Student.objects.filter(student_fees=True)
    total_students = students.count()
    context = {'students': students,'totalStudents':total_students}
    return render(request,'billsManager/fees.html',context)

@login_required
def studentFeeDetails(request,pk):
    studentInfo = Student.objects.get(id_no=int(pk))
    feesInfo =  Fee.objects.get(student=studentInfo)
    if str(request.user) != str(studentInfo.school_username):
        return HttpResponse('Your are not allowed here!!')
    totalFee = int(feesInfo.fee_paid) + int(feesInfo.amount)
    feePaid = int(feesInfo.fee_paid)
    feePending = int(feesInfo.amount)
    context = {"student":studentInfo,"feesInfo":feesInfo,"totalFees":totalFee,"feePaid":feePaid,"feePending":feePending}
    return render(request,'billsManager/studentFeeDetails.html',context)