import shutil
import os
from django.core.management.base import BaseCommand
from competition.models import User, CheckPoint, Team, Membership, UserPosition
from competition.tests.globals_for_tests import Globals as G

class Command(BaseCommand):
    help = "Clean data and load demo data."
    demo_password = G.user1_password
    demo_user_base_name = "TestUser"
    demo_team_base_name = "TestTeam"
    demo_checkpoint_base_name = "TestCheckpoint"
    demo_lat = 57.6864
    demo_lon = 12.0129

    def handle(self, *args, **options):
        print("Purge them all!")
        self.purge_existing_data()
        self.copy_demo_images()
        self.load_demo_data()


    def purge_existing_data(self):
        for user in User.objects.all():
            user.delete()
        for checkpoint in CheckPoint.objects.all():
            checkpoint.delete()
        for team in Team.objects.all():
            team.delete()

    def copy_demo_images(self):
        destination = os.path.join("static", "images", "demo_images")
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        os.mkdir(destination)
        shutil.copy(os.path.join("competition", "static", "images", "DemoPoint.JPG"),
                    os.path.join(destination, "DemoPoint.JPG"))
        shutil.copy(os.path.join("competition", "static", "images", "DemoTeam.jpeg"),
                    os.path.join(destination, "DemoTeam.jpeg"))

    def load_demo_data(self):
        # Admin user:
        User.objects.create_user("admin", password=self.demo_password, is_staff=True, is_superuser=True)

        for i in range(1,7):
            user = User.objects.create_user(f"{self.demo_user_base_name}{i}", password=self.demo_password)
            position = UserPosition.objects.get(user=user)
            position.gps_lon = self.demo_lon+0.01*i - 0.05
            position.gps_lat = self.demo_lat + 0.01 * i - 0.005
            position.save()

            if i % 2:
                checkpoint = CheckPoint.objects.create(name=f"{self.demo_checkpoint_base_name}{1+i//2}",
                                                       photo="demo_images/DemoPoint.JPG",
                                                       gps_lon=self.demo_lon+0.01*i,
                                                       gps_lat=self.demo_lat+0.01*i)
                team = Team.objects.create(name=f"{self.demo_team_base_name}{1+i//2}", photo="demo_images/DemoTeam.jpeg")
                if i != 5:
                    team.confirmed=True
                    team.save()
            membership = Membership.objects.get(user=user)
            membership.team = team
            membership.save()

