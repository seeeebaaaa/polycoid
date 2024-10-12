from django.shortcuts import render
import random


def index(request):
  context = {"randomNumber":random.randint(0,100)}
  return render(request, "filmliste/index.html", context)
