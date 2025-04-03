from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    id_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png')
    date_joined_chama = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def total_contributions(self):
        from contributions.models import Contribution
        return Contribution.objects.filter(user=self.user).aggregate(models.Sum('amount'))['amount__sum'] or 0
    
    def active_loans(self):
        from loans.models import Loan
        return Loan.objects.filter(user=self.user, status__in=['PENDING', 'APPROVED']).count()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

