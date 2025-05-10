from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
# Create your models here.

# practicing Foreign key relationship
# create a model for headteacher 
class HeadTeacher(models.Model):
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    date_appointed = models.DateField()

    def __str__(self):
        return self.name

# creating a model for the fee-structure
class FeeStructure(models.Model):
    grade = models.IntegerField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, blank=True)
    effective_from = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Grade {self.grade} - {self.amount} (from {self.effective_from})"
      
# creating a model for students
class Student(models.Model):
   name = models.CharField(max_length=100)
   age = models.IntegerField()
   grade = models.IntegerField() 
   guardian_name = models.CharField(max_length=100)
   guardian_address = models.TextField() 

   # updating the student model to include a foreign key relationship with the HeadTeacher model
   headteacher = models.ForeignKey('HeadTeacher', on_delete=models.PROTECT, related_name='students')
   
   fee_structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True, blank=True)
   
   def save(self, *args, **kwargs):
        # Automatically assign fee structure based on grade
        if not self.fee_structure:
            self.fee_structure = FeeStructure.objects.filter(grade=self.grade).first()
        
        # Automatically assign the latest HeadTeacher if not provided
        if not self.headteacher:
            self.headteacher = HeadTeacher.objects.latest('id')  # Get the latest HeadTeacher by ID
            
        super().save(*args, **kwargs)

   def __str__(self):
       return self.name

@receiver(post_save, sender=Student)
def create_payment_plan(sender, instance, created, **kwargs):
    if created and instance.fee_structure:
        PaymentPlan.objects.create(
            student=instance,
            total_fee=instance.fee_structure.amount
        )
        
# incorporating other models targetted to payments of the fees ie payment plan and payment
#Payment plan acting as a summary of the student's payment for the term
class PaymentPlan(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='payment_plan')
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        self.balance = self.total_fee - self.amount_paid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment Plan for {self.student.name} - Total Fee: {self.total_fee}, Amount Paid: {self.amount_paid}, Balance: {self.balance}"
    
# Payment model to record individual payments made by the student
class Payment(models.Model):
    payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.payment_plan.student.name} on {self.date}"

@receiver(post_save, sender=Payment)
def update_payment_plan_on_save(sender, instance, **kwargs):
    payment_plan = instance.payment_plan
    payment_plan.amount_paid = sum(payment.amount for payment in payment_plan.payments.all())
    payment_plan.save()


@receiver(post_delete, sender=Payment)
def update_payment_plan_on_delete(sender, instance, **kwargs):
    payment_plan = instance.payment_plan
    payment_plan.amount_paid = sum(payment.amount for payment in payment_plan.payments.all())
    payment_plan.save()



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

