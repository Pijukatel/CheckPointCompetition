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
    photo = models.ImageField(upload_to="checkpoints")


class Team(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    photo = models.ImageField(upload_to="teams", null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    confirmation_date = models.DateTimeField(auto_now=True)
    deny_reason = models.CharField(max_length=150, blank=True, default="")

    def get_absolute_url(self):
        return reverse("team", kwargs={"pk": self.name})

    @classmethod
    def get_objects_to_confirm(cls, **kwargs):
        """Get confirmation queue for this model."""
        return cls.objects.filter(confirmed=False, name=kwargs["pk"]).exclude(photo='')


class Point(models.Model):
    photo = models.ImageField(upload_to="points")
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    checkpoint = models.ForeignKey(
        CheckPoint, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    confirmation_date = models.DateTimeField(auto_now=True)
    visit_date = models.DateTimeField(auto_now_add=True)
    deny_reason = models.CharField(max_length=150, blank=True, default="")

    def get_absolute_url(self):
        return reverse("point", kwargs={"team": self.team_id,
                                        "checkpoint": self.checkpoint_id})

    @classmethod
    def get_objects_to_confirm(cls, **kwargs):
        """Get confirmation queue for this model."""
        return cls.objects.filter(confirmed=False,
                                  team=kwargs["team"],
                                  checkpoint=kwargs["checkpoint"]).exclude(photo='')

    class Meta:
        """Unique point for each team and checkpoint."""
        constraints = [
            models.UniqueConstraint(
                fields=["team", "checkpoint"],
                name="%(app_label)s_%(class)s_one_per_team_and_checkpoint"),
        ]


class Membership(models.Model):
    """Intermediate model for user being able to be member of a group."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

class Invitation(models.Model):
    """Intermediate model for user being able to be member of a group."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        """Unique invitation for each team and user."""
        constraints = [
            models.UniqueConstraint(
                fields=["user", "team"],
                name="%(app_label)s_%(class)s_one_per_team_and_user"),
        ]


class UserPosition(models.Model):
    """Intermediate model to add position to each user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gps_lat = models.FloatField(default=0)
    gps_lon = models.FloatField(default=0)
    time = models.DateTimeField(auto_now=True)

    def __eq__(self, other):
        if (isinstance(other, self.__class__)
                and self.user == other.user
                and self.gps_lat == other.gps_lat
                and self.gps_lon == other.gps_lon):
            return True

    def __hash__(self):
        return hash((self.user_id, self.gps_lat, self.gps_lon))


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Using signals to create membership when user is created."""
    if created:
        Membership.objects.create(user=instance)
        UserPosition.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Using signals to save membership when user is saved."""
    if not instance.is_superuser:
        instance.membership.save()


@receiver(post_save, sender=Membership)
def after_membership_save(sender, instance, **kwargs):
    delete_empty_teams()


@receiver(post_save, sender=Team)
def after_team_save(sender, instance, **kwargs):
    """Once team is confirmed prepare all it's points.

    This should happen only once as team should be locked for editing after confirmation."""
    if instance.confirmed:
        create_team_points_for_each_checkpoint(instance)


def create_team_points_for_each_checkpoint(team):
    """This function creates empty points for each checkpoint."""
    for checkpoint in CheckPoint.objects.all():
        Point(team=team, checkpoint=checkpoint).save()


def delete_empty_teams():
    """Using signals to check for teams without membership and deleting them."""
    inhabited_teams = {membership.team for membership in Membership.objects.filter(team__membership__isnull=False)}
    all_teams = set(Team.objects.all())
    empty_teams = all_teams - inhabited_teams
    for team in empty_teams:
        team.delete()
