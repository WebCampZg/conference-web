from collections import defaultdict
from pprint import pprint

from django.shortcuts import render

def list_schedule(request):
    return render(request, 'schedule/schedule.html')

