from django.db import models
from studentsManager.models import Student
# Create your models here.
class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('pending', 'Pending')])
    
    def __str__(self):
        return f"{self.student.name} - {self.amount} due on {self.due_date}"

class busFees(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    bus_amount = models.DecimalField(max_digits=100,decimal_places=2)
    due_date = models.DateField()
    last_Paid = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.amount} due on {self.due_date}"