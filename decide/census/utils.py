from voting.models import Voting
from django.utils import timezone


def check_str_is_int(string):
    try:
        int(string)

        return True

    except ValueError:
        return False


def check_voting_is_started(id):

    votings = Voting.objects.filter(pk=id)
    is_started=True

    for voting in votings:
        start_date = voting.start_date

        if start_date is None:
            is_started=False

        elif start_date > timezone.now():
            is_started=False

    return is_started

