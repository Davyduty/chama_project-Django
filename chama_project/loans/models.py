from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Loan(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('PAID', 'Paid')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=255)
    application_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    approved_date = models.DateTimeField(blank=True, null=True)
    repayment_period = models.IntegerField(help_text="Repayment period in months")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-application_date']
    
    def __str__(self):
        return f"{self.user.username} - ${self.amount} ({self.get_status_display()})"
    
    def total_repayment_amount(self):
        interest = (self.amount * self.interest_rate / 100) * (self.repayment_period / 12)
        return self.amount + interest
    
    def monthly_payment(self):
        if self.repayment_period > 0:
            return self.total_repayment_amount() / self.repayment_period
        return 0

class LoanRepayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    payment_method = models.CharField(max_length=50, choices=[
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('MOBILE_MONEY', 'Mobile Money'),
        ('CHEQUE', 'Cheque')
    ], default='CASH')
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Repayment of ${self.amount} for {self.loan}"

