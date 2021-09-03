from django.contrib.auth.models import User
from django.urls import path
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView

from .models import CheckPoint, Team, Point
from .views import (home, RegisterUser, login_page, logout_link, UserDetail, UserUpdate, UserDelete, TeamDetail,
                    TeamCreate, leave_team, add_team_member, TeamUpdate, TeamDelete, PointPhotoConfirmationView,
                    TeamPhotoConfirmationView, PointUpdate, PointDetail, PointList, CheckPointDetail, checkpoint_view)
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
    path("checkpoints/",
         ListView.as_view(model=CheckPoint, template_name="competition/checkpoint_list.html"), name="checkpoints"),
    path("checkpoint/<str:pk>/", checkpoint_view, name="checkpoint"),
    #path("checkpoint/<str:pk>/", CheckPointDetail.as_view(), name="checkpoint"),

    path("point/photo-confirm/", RedirectToTopOfConfirmationQueue.as_view(model=Point),
         name="point_photo_confirm_queue"),
    path("point/<str:team>/<str:checkpoint>/photo-confirm/", PointPhotoConfirmationView.as_view(),
         name="point_photo_confirm"),
    path("points/<str:team>/", PointList.as_view(), name="points"),
    path("point/<str:team>/<str:checkpoint>/update/", PointUpdate.as_view(), name="point_update"),
    path("point/<str:team>/<str:checkpoint>/", PointDetail.as_view(), name="point"),
    path("point/<str:pk>/update/", UpdateView.as_view(model=Point), name="point_update"),
    path("point/<str:pk>/delete/", DeleteView.as_view(model=Point), name="point_delete"),
    path("team/create/", TeamCreate.as_view(), name="team_create"),
    path("team/leave/", leave_team, name="leave_team"),
    path("team/photo-confirm/", RedirectToTopOfConfirmationQueue.as_view(model=Team), name="team_photo_confirm_queue"),
    path("team/<str:pk>/photo-confirm/", TeamPhotoConfirmationView.as_view(), name="team_photo_confirm"),
    path("team/<str:pk>/", TeamDetail.as_view(), name="team"),
    path("team/<str:pk>/update/", TeamUpdate.as_view(), name="team_update"),
    path("team/<str:pk>/delete/", TeamDelete.as_view(), name="team_delete"),
    path("team/<str:pk>/add_member/", add_team_member, name="add_team_member"),
    path("teams/", ListView.as_view(model=Team, template_name="competition/team_list.html"), name="teams"),
]
