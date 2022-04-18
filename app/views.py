from urllib import response
from django.shortcuts import render
from django.http.response import JsonResponse

from app.models import Guest
# Create your views here.

# without Rest and no model query FBV
def no_rest_no_model(request):
    guests = [
        {
            'id':1,
            "name":'younis',
            "mobile":7410852,
        },
        {
            'id':2,
            "name":'saeed',
            "mobile":8520,
        },
    ]
    return JsonResponse(guests, safe=False)


# 2 no rest but from model
def no_rest_from_model(request):

    guest = Guest.objects.all()
    response = {
        'data':list(guest.values())
    }
    return JsonResponse(response , safe=False)

# List == GET
# Create == POST
# Update == PUT
# Delete destroy == DELETE

