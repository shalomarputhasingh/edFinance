from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from billsManager.models import Fee
from studentsManager.models import Student
from billsManager.models import busFees
from billsManager.models import transactionHistroy
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import get_object_or_404
@login_required
def createFees(request, pk):
    studentInfo = get_object_or_404(Student, id_no=pk)  # Fetch the Student or return a 404 if not found

    if request.method == 'POST':
        amountEntered = request.POST.get("fees-pendingAmount")
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
                pendingAmount=amountEntered,
                due_date=dueDateEntered,
                total_fees = amountEntered,
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
    transHistory = transactionHistroy.objects.filter(student = studentInfo,typeFees="fees").order_by('-last_Paid').values()
    if str(request.user) != str(studentInfo.school_username):
        return HttpResponse('Your are not allowed here!!')
    totalFee = feesInfo.total_fees
    feePaid = int(feesInfo.fee_paid)
    feePending = int(feesInfo.pendingAmount)
    context = {"student":studentInfo,"feesInfo":feesInfo,"totalFees":totalFee,"feePaid":feePaid,"feePending":feePending,"transReports":transHistory}
    return render(request,'billsManager/studentFeeDetails.html',context)

@login_required
def studentBillingFees(request,pk):
    studentInfo = Student.objects.get(id_no=int(pk))
    feesInfo =  Fee.objects.get(student=studentInfo)
    
    if str(request.user) != str(studentInfo.school_username):
        return HttpResponse('Your are not allowed here!!')
    #Handles the Billing for the Fees for that particular student
    if request.method == "POST":
        amountEntered = request.POST.get("amount_entered")
        if(feesInfo.pendingAmount>=int(amountEntered)):
            feesInfo.pendingAmount = feesInfo.pendingAmount - int(amountEntered)
            feesInfo.fee_paid = feesInfo.fee_paid + int(amountEntered)
            if(feesInfo.pendingAmount == 0):
                feesInfo.status = "paid"
            feesInfo.save()
            transHistroy = transactionHistroy(
                student = studentInfo,
                pendingAmount = feesInfo.pendingAmount,
                paid = amountEntered,
                typeFees = "fees"
            )
            transHistroy.save()
            messages.success(request, 'Payment Successful')
        else:
            messages.error(request, 'Payment Failed: Invaild Billing pendingAmount')
        return redirect("feeDetails",pk)
    totalFee = int(feesInfo.fee_paid) + int(feesInfo.pendingAmount)
    feePaid = int(feesInfo.fee_paid)
    feePending = int(feesInfo.pendingAmount)
    context = {"student":studentInfo,"feesInfo":feesInfo,"totalFees":totalFee,"feePaid":feePaid,"feePending":feePending}
    return render(request,'billsManager/makingFeesPayment.html',context)

@login_required
def createBusFees(request, pk):
    studentInfo = get_object_or_404(Student, id_no=pk)  # Fetch the Student or return a 404 if not found
    feesInfo  = Fee.objects.get(student = studentInfo)
    if request.method == 'POST':
        amountEntered = request.POST.get("fees-amount")
        dueDateEntered = request.POST.get("due-date")
        feesInfo  = Fee.objects.get(student = studentInfo)
        # Check if the required fields are present
        if not amountEntered or not dueDateEntered:
            return render(request, 'billsManager/createBusFees.html', {
                'student': studentInfo,
                'error': 'All fields are required.'
            })
        
        # Try to create and save the Fee instance
        try:
            busFee = busFees(
                student=studentInfo,  # Link the Student object directly
                bus_amount=amountEntered,
                due_date=dueDateEntered,
                total_fees = amountEntered
            )
            busFee.save()  # Save the busFee instance to the database
            
            feesInfo.bus_fees = True
            feesInfo.save()  # Save the updated Fees instance
            
            return redirect('fees')  # Redirect to the students page after successful creation

        except Exception as e:
            # Log the exception or print it out for debugging
            print(f"Error saving fee: {e}")
            return render(request, 'billsManager/createVanFees.html', {
                'student': studentInfo,
                'error': 'There was an error processing your request. Please try again.'
            })
    
    # Render the form if the request method is GET
    if feesInfo.bus_fees == False:
        return render(request, 'billsManager/createBusFees.html', {'student': studentInfo})
    else:
        return redirect('students')
    
@login_required
def studentVanFeeDetails(request,pk):
    studentInfo = Student.objects.get(id_no=int(pk))
    feesInfo =  busFees.objects.get(student=studentInfo)
    transHistory = transactionHistroy.objects.filter(student = studentInfo,typeFees="vanFees").order_by('-last_Paid').values()
    if str(request.user) != str(studentInfo.school_username):
        return HttpResponse('Your are not allowed here!!')
    totalFee = feesInfo.total_fees
    feesPaidSoFar = feesInfo.total_fees - feesInfo.bus_amount 
    feePaid = feesPaidSoFar
    feePending = int(feesInfo.bus_amount)
    context = {"student":studentInfo,"feesInfo":feesInfo,"totalFees":totalFee,"feePaid":feePaid,"feePending":feePending,"transReports":transHistory}
    return render(request,'billsManager/studentVanFeeDetails.html',context)
@login_required
def studentVanBillingFees(request,pk):
    studentInfo = Student.objects.get(id_no=int(pk))
    feesInfo =  busFees.objects.get(student=studentInfo)
    
    if str(request.user) != str(studentInfo.school_username):
        return HttpResponse('Your are not allowed here!!')
    #Handles the Billing for the Fees for that particular student
    if request.method == "POST":
        amountEntered = request.POST.get("amount_entered")
        if(feesInfo.bus_amount>=int(amountEntered)):
            feesInfo.bus_amount = feesInfo.bus_amount - int(amountEntered)
            feesInfo.save()
            transHistroy = transactionHistroy(
                student = studentInfo,
                pendingAmount = feesInfo.bus_amount,
                paid = amountEntered,
                typeFees = "vanFees"
            )
            transHistroy.save()
            messages.success(request, 'Payment Successful')
        else:
            messages.error(request, 'Payment Failed: Invaild Billing pendingAmount')
        return redirect("vanFeeDetails",pk)
    totalFee = feesInfo.total_fees
    feePaid = feesInfo.bus_amount
    feePending = feesInfo.bus_amount
    context = {"student":studentInfo,"feesInfo":feesInfo,"totalFees":totalFee,"feePaid":feePaid,"feePending":feePending}
    return render(request,'billsManager/makingFeesPayment.html',context)





