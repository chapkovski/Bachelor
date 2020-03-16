from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range

from .models import Constants


class WorkPage(Page):
    timer_text = 'Time left to complete the task:'
    timeout_seconds = 60


page_sequence = [
    WorkPage,
]