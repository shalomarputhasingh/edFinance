from django.db import models
from usersAuth.models import User  # Adjust the import based on your project structure

class Student(models.Model):
    id_no = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    student_class = models.CharField(max_length=50)
    parents_phone_number = models.CharField(max_length=20)
    dob = models.DateField()
    school = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students')
    school_name = models.CharField(max_length=100, editable=False)  # Automatically populated
    school_username = models.CharField(max_length=30, editable=False)  # Automatically populated

    def __str__(self):
        return f"{self.student_name} - {self.id_no}"

    def save(self, *args, **kwargs):
        if self.school:
            self.school_name = self.school.school_name  # Get the school name from the linked User instance
            self.school_username = self.school.username  # Get the username from the linked User instance
        super().save(*args, **kwargs)
