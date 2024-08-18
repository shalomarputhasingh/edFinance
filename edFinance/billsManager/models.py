from django.db import models
from studentsManager.models import Student
# Create your models here.
class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    pendingAmount = models.DecimalField(max_digits=100, decimal_places=2)
    total_fees = models.DecimalField(max_digits=100, decimal_places=2,null=False)
    due_date = models.DateField()
    fee_paid = models.DecimalField(default=0,max_digits=100, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('pending', 'Pending')])
    bus_fees = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.student.name} - {self.pendingAmount} due on {self.due_date}"

class busFees(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_fees = models.DecimalField(max_digits=100,decimal_places=2)
    bus_amount = models.DecimalField(max_digits=100,decimal_places=2)
    due_date = models.DateField()
    last_Paid = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.bus_amount} due on {self.due_date}"
    
class transactionHistroy(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    trans_id = models.AutoField(auto_created=True,null=False,primary_key=True)
    pendingAmount = models.DecimalField(max_digits=100,decimal_places=2)
    paid =  models.DecimalField(max_digits=100,decimal_places=2)
    typeFees = models.CharField(max_length=20, choices=[('fees', 'Fees'), ('vanFees', 'VanFees')])
    last_Paid = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.pendingAmount} due on {self.last_paid}"