from django.contrib import admin
from .models import Loan, LoanRepayment

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'purpose', 'application_date', 'status', 'repayment_period')
    list_filter = ('status', 'application_date')
    search_fields = ('user__username', 'purpose', 'notes')
    date_hierarchy = 'application_date'

@admin.register(LoanRepayment)
class LoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'amount', 'payment_date', 'payment_method', 'transaction_id')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('loan__user__username', 'transaction_id', 'notes')
    date_hierarchy = 'payment_date'

