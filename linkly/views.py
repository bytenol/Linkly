from django.shortcuts import render, redirect
from django.http import JsonResponse
from random import randrange
import json

from .models import LinklyUrl


def getRandomString(max_length = 6):
    alpha = "labcmdvebfgahpnijkqlhomncorpqgrsitudfvwxeyjzk"
    res = ""
    for _ in range(max_length):
        v = randrange(0, len(alpha) - 1)
        res += alpha[v]
    return res


def home(request):
    context = {}
    return render(request, "linkly/index.html", context)


"""This view is called by the Covert button to add a new link or 
get an existing link from the database

It tries to create a shortened url a maximum of 10 times for uniqueness
untill the first unique shortened link is found"""
def addUrl(request):
    data = {}
    if request.method == "POST":
        body = json.loads(request.body)
        f_url = body.get("fromUrl")

        if f_url == "": 
            return JsonResponse({ "error": "Invalid Url" })

        try:
            m = LinklyUrl.objects.get(fromUrl = f_url)
            data["toUrl"] = m.toUrl
        except LinklyUrl.DoesNotExist:
            for _ in range(10):            
                t_url = getRandomString()
                try:
                    m = LinklyUrl.objects.get(toUrl = t_url)
                except LinklyUrl.DoesNotExist:
                    break

            m = LinklyUrl.objects.create(fromUrl = f_url, toUrl = t_url)
            m.save()
            data["toUrl"] = t_url
        return JsonResponse(data)

    return JsonResponse({})



"""This view redirects all shortened to their original link
otherwise, it redirect back to the Linkly's Homepage"""
def redirectUrl(request, t_url):
    try:
        m = LinklyUrl.objects.get(toUrl = t_url)
    except LinklyUrl.DoesNotExist:
        return redirect("linkly/index.html")
    
    return redirect(m.fromUrl)