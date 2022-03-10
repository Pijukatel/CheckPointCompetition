# Generated by Django 3.2.5 on 2022-03-10 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckPoint',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('gps_lat', models.FloatField()),
                ('gps_lon', models.FloatField()),
                ('photo', models.ImageField(upload_to='checkpoints')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='teams')),
                ('confirmed', models.BooleanField(default=False)),
                ('confirmation_date', models.DateTimeField(auto_now=True)),
                ('deny_reason', models.CharField(blank=True, default='', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='UserPosition',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('gps_lat', models.FloatField(default=0)),
                ('gps_lon', models.FloatField(default=0)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='points')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('confirmation_date', models.DateTimeField(auto_now=True)),
                ('visit_date', models.DateTimeField(auto_now_add=True)),
                ('deny_reason', models.CharField(blank=True, default='', max_length=150)),
                ('checkpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.checkpoint')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.team')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='competition.team')),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='point',
            constraint=models.UniqueConstraint(fields=('team', 'checkpoint'), name='competition_point_one_per_team_and_checkpoint'),
        ),
        migrations.AddConstraint(
            model_name='invitation',
            constraint=models.UniqueConstraint(fields=('user', 'team'), name='competition_invitation_one_per_team_and_user'),
        ),
    ]
