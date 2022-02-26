from django.contrib.auth.models import User
from django.urls import path
from django.views.generic import ListView

from .api.views import user_positions, checkpoint_positions, memberships, current_user_pos, teams, points, user, score
from .models import CheckPoint, Team, Point
from .views import (home, RegisterUser, login_page, logout_link, UserDetail, UserUpdate, UserDelete, TeamDetail,
                    TeamCreate, leave_team, add_team_member, TeamUpdate, TeamDelete, PointPhotoConfirmationView,
                    TeamPhotoConfirmationView, PointDetail, checkpoint_view,
                    CheckpointList, TeamList, base_map_view)
from .views_generic import RedirectToTopOfConfirmationQueue

urlpatterns = [
    path("", home, name="home"),
    path("accounts/register/", RegisterUser.as_view(), name="register"),
    path("accounts/login/", login_page, name="login"),
    path('accounts/logout/', logout_link, name='logout'),
    path("accounts/user/", UserDetail.as_view(), name="user"),
    path("accounts/users/", ListView.as_view(model=User, template_name="competition/user_list.html"), name="users"),
    path("accounts/user/update/", UserUpdate.as_view(model=User), name="user_update"),
    path("accounts/user/delete/", UserDelete.as_view(), name="user_delete"),
    path("checkpoints/", CheckpointList.as_view(), name="checkpoints"),
    path("checkpoint/<str:pk>/", checkpoint_view, name="checkpoint"),
    path("point/photo-confirm/", RedirectToTopOfConfirmationQueue.as_view(model=Point),
         name="point_photo_confirm_queue"),
    path("point/<str:team>/<str:checkpoint>/photo-confirm/", PointPhotoConfirmationView.as_view(),
         name="point_photo_confirm"),
    path("point/<str:team>/<str:checkpoint>/", PointDetail.as_view(), name="point"),
    path("team/create/", TeamCreate.as_view(), name="team_create"),
    path("team/leave/", leave_team, name="leave_team"),
    path("team/photo-confirm/", RedirectToTopOfConfirmationQueue.as_view(model=Team), name="team_photo_confirm_queue"),
    path("team/<str:pk>/photo-confirm/", TeamPhotoConfirmationView.as_view(), name="team_photo_confirm"),
    path("team/<str:pk>/", TeamDetail.as_view(), name="team"),
    path("team/<str:pk>/update/", TeamUpdate.as_view(), name="team_update"),
    path("team/<str:pk>/delete/", TeamDelete.as_view(), name="team_delete"),
    path("team/<str:pk>/add_member/", add_team_member, name="add_team_member"),
    path("teams/", TeamList.as_view(), name="teams"),
    path("map_base/", base_map_view, name='map_base'),
    path("api/user_positions/", user_positions, name="api_user_positions"),
    path("api/current_user_pos/", current_user_pos, name="api_current_user_pos"),
    path("api/checkpoint_positions/", checkpoint_positions, name="api_checkpoint_positions"),
    path("api/memberships/", memberships, name="api_memberships"),
    path("api/teams/", teams, name="api_teams"),
    path("api/points/", points, name="api_points"),
    path("api/user/", user, name="api_user"),
    path("api/score/", score, name="score"),
]
