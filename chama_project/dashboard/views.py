from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.contrib.auth.models import User
from contributions.models import Contribution
from loans.models import Loan

@login_required
def dashboard_home(request):
    # User's contributions
    user_contributions = Contribution.objects.filter(user=request.user)
    total_contributions = user_contributions.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # User's loans
    user_loans = Loan.objects.filter(user=request.user)
    total_loans = user_loans.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Loan status counts
    loan_status = {
        'pending': user_loans.filter(status='PENDING').count(),
        'approved': user_loans.filter(status='APPROVED').count(),
        'rejected': user_loans.filter(status='REJECTED').count(),
        'paid': user_loans.filter(status='PAID').count(),
    }
    
    # Recent contributions
    recent_contributions = user_contributions.order_by('-date')[:5]
    
    # Recent loans
    recent_loans = user_loans.order_by('-application_date')[:5]
    
    context = {
        'total_contributions': total_contributions,
        'total_loans': total_loans,
        'loan_status': loan_status,
        'recent_contributions': recent_contributions,
        'recent_loans': recent_loans,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def admin_dashboard(request):
    # Only allow staff/admin users
    if not request.user.is_staff:
        return dashboard_home(request)
    
    # Total users
    total_users = User.objects.count()
    
    # Total contributions
    all_contributions = Contribution.objects.all()
    total_contributions = all_contributions.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Total loans
    all_loans = Loan.objects.all()
    total_loans = all_loans.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Loan status counts
    loan_status = {
        'pending': all_loans.filter(status='PENDING').count(),
        'approved': all_loans.filter(status='APPROVED').count(),
        'rejected': all_loans.filter(status='REJECTED').count(),
        'paid': all_loans.filter(status='PAID').count(),
    }
    
    # Recent contributions
    recent_contributions = all_contributions.order_by('-date')[:10]
    
    # Recent loans
    recent_loans = all_loans.order_by('-application_date')[:10]
    
    context = {
        'total_users': total_users,
        'total_contributions': total_contributions,
        'total_loans': total_loans,
        'loan_status': loan_status,
        'recent_contributions': recent_contributions,
        'recent_loans': recent_loans,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def admin_loans(request):
    # Only allow staff/admin users
    if not request.user.is_staff:
        return dashboard_home(request)
    
    # Get all loans
    all_loans = Loan.objects.all().select_related('user')
    
    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter and status_filter != 'ALL':
        all_loans = all_loans.filter(status=status_filter)
    
    context = {
        'loans': all_loans,
        'status_filter': status_filter,
    }
    return render(request, 'dashboard/admin_loans.html', context)

@login_required
def user_details(request, user_id):
    # Only allow staff/admin users
    if not request.user.is_staff:
        return dashboard_home(request)
    
    user = User.objects.get(id=user_id)
    
    # User's contributions
    user_contributions = Contribution.objects.filter(user=user)
    total_contributions = user_contributions.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # User's loans
    user_loans = Loan.objects.filter(user=user)
    total_loans = user_loans.aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'user_detail': user,
        'total_contributions': total_contributions,
        'total_loans': total_loans,
        'contributions': user_contributions,
        'loans': user_loans,
    }
    return render(request, 'dashboard/user_details.html', context)

