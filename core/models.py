from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
        ('Ceso_Staff', 'CESO Staff'),
        ('IT Staff', 'IT Staff'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')
    id_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=50, blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Activity(models.Model):
    STATUS_CHOICES = [
        ('Ongoing', 'Ongoing'),
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=200)
    conducted_by = models.CharField(max_length=200)
    faculty = models.ManyToManyField(User, related_name='activity_faculty')
    students = models.ManyToManyField(User, related_name='activity_students')
    staff = models.ManyToManyField(User, related_name='activity_staff')
    attachment = models.FileField(upload_to='activity_attachments/', null=True, blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    last_edited_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    fees_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
