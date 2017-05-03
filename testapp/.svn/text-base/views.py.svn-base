from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .tasks  import hello_world


def index(request):
    hello_world.apply_async(("1", "2"), countdown=10)
    return HttpResponse("haha")
