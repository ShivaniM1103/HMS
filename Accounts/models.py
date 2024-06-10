from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Define a validator for the phone number
phone_validator = RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits.")
# Create your models here.


class User(AbstractUser):
    is_doctor= models.BooleanField('Is doctor', default=False)
    is_patient = models.BooleanField('Is patient', default=False)
    is_pharmacist= models.BooleanField('Is pharmacist', default=False)

# shifts=[
#     ('Morning','Morning'),
#     ('Afternoon','Afternoon'),
# ]
class Departments(models.Model):
    dname=models.CharField(max_length=50)
    No_of_doctors=models.PositiveIntegerField(default=0)
    description = models.TextField(default="We have skilled doctors")
    phoneno = models.CharField(max_length=10, validators=[phone_validator], default='0000000000')
    def __str__(self):
        return "{}".format(self.dname)
        
class Bed(models.Model):
    dept = models.OneToOneField(Departments, on_delete=models.CASCADE)
    Ebed = models.PositiveIntegerField(default=0)
    Gbed = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.dept.dname} Em. bed:{self.Ebed}, Gen Bed:{self.Gbed}"


class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='Userpics')
    address = models.CharField(max_length=40)
    phoneno = models.CharField(max_length=10, validators=[phone_validator], default='0000000000')
    department= models.ForeignKey(Departments, on_delete=models.CASCADE)
    status=models.BooleanField(default=False) #whether he/she is in cabin or not
    # shift=models.CharField(max_length=50,choices=shifts,default='Morning')
    @property
    def get_name(self):
        return "{} {}".format(self.user.first_name,self.user.last_name)
    @property
    def get_id(self):
        return self.user.id
    # @property
    # def get_dept(self):
    #     return self.Department.dname
    def __str__(self):
        return "{} ({})".format(self.user.username,self.department)
    
class Pharmacist(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='Userpics')
    address = models.CharField(max_length=40)
    phoneno = models.CharField(max_length=10, validators=[phone_validator], default='0000000000')
    # shift=models.CharField(max_length=50,choices=shifts,default='Morning')
    @property
    def get_name(self):
        return "{} {}".format(self.user.first_name,self.user.last_name)
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{}".format(self.user.username)
    
class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='Userpics')
    address = models.CharField(max_length=40)
    phoneno = models.CharField(max_length=10, validators=[phone_validator], default='0000000000')
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{}".format(self.user.first_name+''+self.user.last_name)
    