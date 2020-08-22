from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import path, reverse
from django.shortcuts import render


import random
from collections import defaultdict
import os
from django.shortcuts import redirect

import logging


def tmp(request):
    return render(request, "base.html")


def about_us(request):
    return render(request, "about_us.html")

urlpatterns = [
    path("tmp", tmp, name="tmp"),
    path("about_us", about_us, name="about_us")
]
