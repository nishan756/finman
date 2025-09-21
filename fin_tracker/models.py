from django.db import models
from django_summernote.fields import SummernoteTextField
import uuid
from django.utils.timezone import now
from session.models import CustomUser
# Create your models here.

SEMESTER_LIST = [
    '1st',
    '2nd',
    '3rd',
    '4th',
    '5th',
    '6th',
    '7th',
    '8th',
    'Ex',
]

SHIFT_LIST = [
    '1st',
    '2nd'
]

SEM_CHOICES = [(sem , sem) for sem in SEMESTER_LIST]
SHIFT_CHOICES = [(shift , shift) for shift in SHIFT_LIST]


class Department(models.Model):
    club = models.ForeignKey(CustomUser,on_delete = models.CASCADE,blank = True,null = True)
    name = models.CharField(max_length = 100)
    small_name = models.CharField(max_length = 10,blank = True,null = True)

    def __str__(self):
        return self.name
    
class Session(models.Model):
    club = models.ForeignKey(CustomUser,on_delete = models.CASCADE,blank = True,null = True)
    session = models.CharField(max_length = 10)

    def __str__(self):
        return self.session

class Member(models.Model):
    club = models.ForeignKey(CustomUser,on_delete = models.CASCADE,blank = True,null = True)
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False) 
    name = models.CharField(max_length = 100)
    roll = models.PositiveIntegerField(unique = True)
    semester = models.CharField(max_length = 4,choices = SEM_CHOICES)
    shift = models.CharField(choices = SHIFT_CHOICES,max_length = 4,blank = True,null = True)
    session = models.ForeignKey(Session,on_delete = models.SET_NULL,blank = True , null = True)
    department = models.ForeignKey(Department , on_delete = models.SET_NULL,null = True,blank = True)
    email = models.EmailField(unique = True)
    contact = models.CharField(max_length = 11,unique = True)
    joined_at = models.DateField(blank = True,null = True)

    class Meta:
        ordering = ['-joined_at',]
        

    def __str__(self):
        return f'{self.name} - {self.semester}-{self.shift}-{self.department.small_name}'
    
    

class PaymentContext(models.Model):
    club = models.ForeignKey(CustomUser,on_delete = models.CASCADE,blank = True,null = True)
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False) 
    title = models.CharField(max_length = 300)
    start_date = models.DateTimeField(verbose_name = 'Started from')
    end_date = models.DateTimeField(verbose_name = 'End on')
    amount = models.PositiveIntegerField()
    detail = SummernoteTextField(blank = True)
    is_active = models.BooleanField(default = False)
    posted_at = models.DateTimeField(default = now,blank = True,null = True)

    class Meta:
        ordering = ['-posted_at',]

    def __str__(self):
        return f'{self.title} - {self.start_date.date()}'
    
    
    

class MemberTransactionDetail(models.Model):
    club = models.ForeignKey(CustomUser,on_delete = models.CASCADE,blank = True,null = True)
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    context = models.ForeignKey(PaymentContext,verbose_name = 'Payment for',on_delete = models.SET_NULL,null = True) 
    member = models.ForeignKey(Member,on_delete = models.CASCADE)
    amount = models.PositiveIntegerField()
    account_no = models.CharField(max_length = 30)
    transaction_id = models.CharField(max_length = 20,unique = True)
    is_paid = models.BooleanField(default = False)
    took_loan = models.BooleanField(default = False)
    due = models.PositiveIntegerField(blank = True,null = True,default = 0)
    date = models.DateTimeField(default = now)
    detail = SummernoteTextField(blank = True)

    class Meta:
        ordering = ['-date',]
    def __str__(self):
        return f'{self.member.name} paid for {self.context.title}'
    




TRAN_TYPE = [
    'Income',
    'Expense'
]

TRAN_TYPE_CHOICE = [(type,type) for type in TRAN_TYPE]

class Transaction(models.Model):
    club = models.ForeignKey(CustomUser,on_delete = models.CASCADE,blank = True,null = True)
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    transaction_type = models.CharField(max_length = 9,choices = TRAN_TYPE_CHOICE,verbose_name = 'Transaction Type')
    title = models.CharField(max_length = 300)
    detail = SummernoteTextField(blank = True)
    amount = models.DecimalField(max_digits = 8,decimal_places = 2)
    member_transaction = models.ForeignKey(MemberTransactionDetail,on_delete = models.CASCADE,blank = True,null = True)
    date = models.DateField(default = now)

    class Meta:
        ordering = ['-date',]
    
    def __str__(self):
        return f'{self.title} - {self.date}'
    
        