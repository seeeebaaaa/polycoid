from django.shortcuts import render
from django.http import HttpResponseRedirect
import random
from .forms import NameForm


def index(request):
  context = {"randomNumber":random.randint(0,100)}
  return render(request, "filmliste/index.html", context)


# the view to handle login & register
def login(request):
  # if used to send content
  if request.method == "POST":
    form = NameForm(request.POST)
    if form.is_valid():
      print(f"yay, {form.cleaned_data}")
      return render(request,"filmliste/index.html",{"form":form})
  # if sth is wrong, GET or not valid, return normal view
  form = NameForm()
  return render(request,"filmliste/login.html",{"form":form})