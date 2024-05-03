from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    # pylint: disable=missing-function-docstring
    # pylint: disable=unused-argument
    return HttpResponse("Hello, Django!")
