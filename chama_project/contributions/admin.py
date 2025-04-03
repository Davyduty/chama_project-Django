from django.contrib import admin
from .models import Contribution

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'payment_method', 'transaction_id')
    list_filter = ('payment_method', 'date')
    search_fields = ('user__username', 'transaction_id', 'notes')
    date_hierarchy = 'date'


