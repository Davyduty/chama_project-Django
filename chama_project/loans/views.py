from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Loan, LoanRepayment
from .forms import LoanApplicationForm, LoanRepaymentForm, LoanStatusUpdateForm
from contributions.models import Contribution

@login_required
def loan_list(request):
    loans = Loan.objects.filter(user=request.user)
    total_loans = loans.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get all users' loans for the table
    all_users_loans = Loan.objects.all().select_related('user')
    users_loans = {}
    
    for loan in all_users_loans:
        username = loan.user.username
        if username in users_loans:
            users_loans[username]['amount'] += loan.amount
            users_loans[username]['count'] += 1
        else:
            users_loans[username] = {
                'user': loan.user,
                'amount': loan.amount,
                'count': 1
            }
    
    context = {
        'loans': loans,
        'total_loans': total_loans,
        'users_loans': users_loans.values()
    }
    return render(request, 'loans/loan_list.html', context)

@login_required
def loan_application(request):
    # Calculate user's contribution total to determine loan eligibility
    user_contributions = Contribution.objects.filter(user=request.user).aggregate(Sum('amount'))
    total_contributions = user_contributions['amount__sum'] or 0
    
    # Calculate maximum loan amount (e.g., 3x their contributions)
    max_loan_amount = total_contributions * 3
    
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user
            
            # Check if loan amount is within eligible amount
            if loan.amount > max_loan_amount:
                messages.error(request, f'Loan amount exceeds your eligible amount of ${max_loan_amount}')
            else:
                loan.save()
                messages.success(request, 'Loan application submitted successfully!')
                return redirect('loans:list')
    else:
        form = LoanApplicationForm()
    
    context = {
        'form': form,
        'total_contributions': total_contributions,
        'max_loan_amount': max_loan_amount
    }
    return render(request, 'loans/loan_application.html', context)

@login_required
def loan_detail(request, pk):
    loan = get_object_or_404(Loan, pk=pk, user=request.user)
    repayments = LoanRepayment.objects.filter(loan=loan)
    total_repaid = repayments.aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_balance = loan.total_repayment_amount() - total_repaid
    
    # For loan repayment
    if request.method == 'POST':
        form = LoanRepaymentForm(request.POST)
        if form.is_valid():
            repayment = form.save(commit=False)
            repayment.loan = loan
            repayment.save()
            
            # Check if loan is fully repaid
            updated_total = total_repaid + repayment.amount
            if updated_total >= loan.total_repayment_amount():
                loan.status = 'PAID'
                loan.save()
                messages.success(request, 'Loan fully repaid!')
            else:
                messages.success(request, f'Repayment of ${repayment.amount} recorded successfully!')
            
            return redirect('loans:detail', pk=loan.pk)
    else:
        form = LoanRepaymentForm(initial={'amount': min(loan.monthly_payment(), remaining_balance)})
    
    context = {
        'loan': loan,
        'repayments': repayments,
        'total_repaid': total_repaid,
        'remaining_balance': remaining_balance,
        'form': form
    }
    return render(request, 'loans/loan_detail.html', context)

@login_required
def update_loan_status(request, pk):
    # This view is for admins only
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard:home')
    
    loan = get_object_or_404(Loan, pk=pk)
    
    if request.method == 'POST':
        form = LoanStatusUpdateForm(request.POST, instance=loan)
        if form.is_valid():
            loan_update = form.save(commit=False)
            if loan_update.status == 'APPROVED' and not loan.approved_date:
                loan_update.approved_date = timezone.now()
            loan_update.save()
            messages.success(request, f'Loan status updated to {loan_update.get_status_display()}')
            return redirect('dashboard:admin_loans')
    else:
        form = LoanStatusUpdateForm(instance=loan)
    
    context = {
        'form': form,
        'loan': loan
    }
    return render(request, 'loans/update_loan_status.html', context)

