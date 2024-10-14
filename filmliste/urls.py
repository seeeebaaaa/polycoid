from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views
from . import api_views

app_name = "filmliste"

urlpatterns = [
    # site views
    path("",views.list_overview, name="index"),
    path("login",views.login_view,name="login"),
    path("logout", views.logout_view, name="logout"),
    path("verify-email/<uidb64>/<token>", views.verify_email, name="verify_email"),
    path("<int:list_id>",views.list_detail,name="detail"),
    # api views
    path("api/button-test-press",api_views.button_test_press,name="button")
]
