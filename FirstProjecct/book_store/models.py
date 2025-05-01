from django.db import models

# Create your models here.

# practicing Foreign key relationship
# create a model for headteacher 
class HeadTeacher(models.Model):
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    date_appointed = models.DateField()

    def __str__(self):
        return self.name

# creating a fee model
class Fee(models.Model):
    GRADE_CHOICES = [(i, f'Grade {i}') for i in range(1, 9)]  
    
    grade = models.IntegerField(choices=GRADE_CHOICES, unique = True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    due_date = models.DateField()
    academic_year = models.CharField(max_length=9)
    
    def __str__(self):
        return f'Grade {self.grade} - GHc{self.amount}'
    
# I am thinking that the grade in both model should be linked together.
# creating a model for students
class Student(models.Model):
   name = models.CharField(max_length=100)
   age = models.IntegerField()
   grade = models.IntegerField(choices=Fee.GRADE_CHOICES) 
   guardian_name = models.CharField(max_length=100)
   guardian_address = models.TextField() 

   # updating the student model to include a foreign key relationship with the HeadTeacher model
   headteacher = models.ForeignKey('HeadTeacher', on_delete=models.PROTECT, related_name='students')

   #updating the student model to include the fee model
   fee = models.ForeignKey('Fee', on_delete=models.SET_NULL, null = True, blank =True)

   def save(self, *args, **kwargs):
       if not self.fee_id and self.grade:
           self.fee = Fee.objects.filter(grade=self.grade).first()
       super().save(*args, **kwargs)
   
   @property
   def amount(self):
    "Get fee amount from linked Fee record"
    return self.fee.amount if self.fee else None
   
   @property
   def due_date(self):
    "Get due_date from linked Fee record"
    return self.fee.due_date if self.fee else None
   
   def __str__(self):
       return self.name
   

# ORM (Object Relational Mapping) is a technique that allows you to interact with a database using Python objects instead of writing raw SQL queries. Django's ORM provides a high-level abstraction for working with databases, making it easier to perform CRUD (Create, Read, Update, Delete) operations on your models.
#In [1]: from book_store.models import Student

#In [2]: student1 = Student.objects.create(name="Peter Piper",age = 3, grade = 3, guardian_name ="Margaret Ofosu-Kwarteng", guardian_address = "0557258671")

#In [3]: student1.save()

#In [4]: student2 = Student.objects.create(name="Maame Nyarko",age = 14, grade = 8, guardian_name ="Getrude Ofosu-Kwarteng", guardian_address = "0242962947")

#In [5]: student2.save()

#In [6]: all_students = Student.objects.all()

#In [7]: for student in all_students:
#   ...:     print(student.name, student.age)
#   ...:
#Peter Piper 3
#Maame Nyarko 14

#In [8]: student = Student.objects.get(id =1)

#In [9]: print(student)
#Peter Piper

#In [10]: student = Student.objects.get(id = 2)

#In [11]: print(student)
#Maame Nyarko

#In [12]: students = Student.objects.filter(grade=2)

#In [13]: print(students)
#<QuerySet []>

# In [15]: students = Student.objects.filter(grade=8)

#In [16]: print(students)
#<QuerySet [<Student: Maame Nyarko>]>

#In [17]: students = Student.objects.get(id = 1)

#In [18]: students.delete()
#Out[18]: (1, {'book_store.Student': 1})

#In [19]: all_students = Student.objects.all()

#In [20]: for student in all_students:
#    ...:     #print(student.name, student.age)
#   ...:
#Maame Nyarko 14

# In this example, i implemented the CRUD operations (CREATE, READ, and DELETE operations) in Django ORM . there is no example of Update though. thus for U.

