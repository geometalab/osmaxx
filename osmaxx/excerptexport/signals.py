from django.core.signals import request_finished
from django.dispatch import receiver

work_after_request_finished = []


def postpone_work_after_request_finished(function, *args, **kwargs):
    work_after_request_finished.append(work(function, *args, **kwargs))


def work(function, *args, **kwargs):
    def do_work():
        return function(*args, **kwargs)
    return do_work


@receiver(request_finished)
def do_postponed_work(sender, **kwargs):
    while work_after_request_finished:
        work = work_after_request_finished.pop()
        work()
