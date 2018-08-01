import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'PUblished recently?'
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    anual_leave_quota = models.IntegerField(default=10)
    anual_leave_remain = models.IntegerField(default=10)
    sick_leave_quota = models.IntegerField(default=10)
    sick_leave_remain = models.IntegerField(default=5)
    #supervisor = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class LeaveRequest(models.Model):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2
    REQUEST_STATUS_CHOIES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
        )
    leave_start_date = models.DateTimeField('leave start')
    leave_end_date = models.DateTimeField('leave end')
    leave_request_status = models.IntegerField(
        choices = REQUEST_STATUS_CHOIES,
        default = PENDING,
        )
    leave_requester = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def leave_days(self):
        delta = self.leave_end_date - self.leave_start_date
        return delta.day

