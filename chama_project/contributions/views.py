from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Contribution
from .forms import ContributionForm

@login_required
def contribution_list(request):
    contributions = Contribution.objects.filter(user=request.user)
    total_contributions = contributions.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get all users' contributions for the table
    all_users_contributions = Contribution.objects.all().select_related('user')
    users_total = {}
    
    for contribution in all_users_contributions:
        username = contribution.user.username
        if username in users_total:
            users_total[username]['amount'] += contribution.amount
            users_total[username]['count'] += 1
        else:
            users_total[username] = {
                'user': contribution.user,
                'amount': contribution.amount,
                'count': 1
            }
    
    context = {
        'contributions': contributions,
        'total_contributions': total_contributions,
        'users_total': users_total.values()
    }
    return render(request, 'contributions/contribution_list.html', context)

@login_required
def make_contribution(request):
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.user = request.user
            contribution.save()
            messages.success(request, f'Contribution of ${contribution.amount} successfully recorded!')
            return redirect('contributions:list')
    else:
        form = ContributionForm()
    
    return render(request, 'contributions/make_contribution.html', {'form': form})

@login_required
def contribution_detail(request, pk):
    contribution = get_object_or_404(Contribution, pk=pk, user=request.user)
    return render(request, 'contributions/contribution_detail.html', {'contribution': contribution})

