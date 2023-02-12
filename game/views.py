
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404,JsonResponse
from django.urls import reverse

from django.core.exceptions import ObjectDoesNotExist

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

# Create your views here.
def home(request):
    context = {}
    return render(request,'home.html',context)


def get_trajectory_data(request):
    # Calculate the trajectory data
    data = {
        0: {'x':10,'y':10},
        1: {'x':100,'y':100},
        2: {'x':20,'y':20},
        # ...
    }
    return JsonResponse(data)