from django.urls import path

from . import views

app_name = "filmliste"

urlpatterns = [
    path("",views.index, name="index"),
    path("login/",views.login,name="login")
]
