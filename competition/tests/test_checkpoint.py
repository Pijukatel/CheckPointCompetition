import pytest
from pytest_django.asserts import assertTemplateUsed
from .globals_for_tests import G
from ..models import CheckPoint
from django.core.exceptions import ValidationError, ObjectDoesNotExist

