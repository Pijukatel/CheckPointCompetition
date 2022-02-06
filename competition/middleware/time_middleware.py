from django.shortcuts import render
from datetime import datetime
from typing import NamedTuple, Callable
from django.contrib import messages

from competition.settings import COUNTDOWN, PRE_REGISTRATION, COMPETITION, ARCHIVED


class Stage(NamedTuple):
    start_time: datetime
    name: str
    callback: Callable


def redirect_to_countdown(request, normal_response):
    messages.add_message(request,
                         messages.INFO,
                         f"Competition will be open for registration: {PRE_REGISTRATION.isoformat()}")

    return render(request, "competition/home.html")


def return_normal_response(request, normal_response):
    return normal_response


stages_start_times = (
    Stage(COUNTDOWN, "countdown", redirect_to_countdown),
    Stage(PRE_REGISTRATION, "pre_registration", return_normal_response),
    Stage(COMPETITION, "competition", return_normal_response),
    Stage(ARCHIVED, "archived", return_normal_response),
)


def get_current_stage(stages_start_times=stages_start_times):
    valid_stages = [stage for stage in stages_start_times if
                    stage.start_time < datetime.now()]
    return max(valid_stages)


def stages(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        normal_response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return get_current_stage().callback(request, normal_response)

    return middleware
