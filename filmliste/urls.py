from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views
from . import api_views

app_name = "filmliste"

urlpatterns = [
    # site views
    path("dev",views.dev,name="dev"),
    path("",views.list_overview, name="index"),
    path("login",views.login_view,name="login"),
    path("logout", views.logout_view, name="logout"),
    path("verify-email/<uidb64>/<token>", views.verify_email, name="verify_email"),
    path("<int:list_id>",views.list_detail,name="list-details"),
    # path("upload",views.upload_profile_picture, name="upload"),
    #  api views
    path("api/button-test-press",api_views.button_test_press,name="button"),
    path("api/add-list",api_views.add_list,name="add-list"),
    path("api/discover-lists",api_views.discover_lists,name="discover-lists")
]
