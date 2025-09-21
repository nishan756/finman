from django.contrib import admin
from .models import Department,Member,MemberTransactionDetail,PaymentContext,Session,Transaction
# Register your models here.

@admin.register(Department)
class DeptAdmin(admin.ModelAdmin):
    list_display = ['name',]

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session',]

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name','roll','department','semester','session','contact','email']
    list_filter = ['department','semester']

@admin.register(MemberTransactionDetail)
class MemTranDetailAdmin(admin.ModelAdmin):
    list_display = ['member','context','amount','account_no','transaction_id','is_paid','took_loan']
    list_filter = ['context','amount','account_no','is_paid','took_loan']

@admin.register(PaymentContext)
class PaymentContextAdmin(admin.ModelAdmin):
    list_display = ['title','start_date','end_date']
    list_filter = ['start_date','end_date']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_type','title','amount','date','member_transaction']
    list_filter = ['transaction_type','date']

    
