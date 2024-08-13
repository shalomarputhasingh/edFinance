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