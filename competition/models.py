from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


# Create your models here.


class CheckPoint(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField()
    gps_lat = models.FloatField()
    gps_lon = models.FloatField()
    photo = models.ImageField(upload_to='checkpoints')


class Point(models.Model):
    photo = models.ImageField(upload_to='points')
    checkpoint = models.ForeignKey(
        CheckPoint, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)


class Team(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    photo = models.ImageField(upload_to='teams', null=True, blank=True)
    confirmed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('team', kwargs={'pk': self.name})


class Membership(models.Model):
    """Intermediate model for user being able to be member of a group."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Using signals to create membership when user is created."""
    if created:
        Membership.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Using signals to save membership when user is saved."""
    if not instance.is_superuser:
        instance.membership.save()


@receiver(post_save, sender=Membership)
def after_membership_save(sender, instance, **kwargs):
    delete_empty_teams()


def delete_empty_teams():
    """Using signals to check for teams without membership and deleting them."""
    inhabited_teams = {membership.team for membership in Membership.objects.filter(team__membership__isnull=False)}
    all_teams = set(Team.objects.all())
    empty_teams = all_teams - inhabited_teams
    for team in empty_teams:
        team.delete()
