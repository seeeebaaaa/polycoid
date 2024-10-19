import random
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from .utils import send_verification_email
from django.contrib.auth.decorators import login_required
from .forms import ProfilePictureForm

User = get_user_model()

def dev(request):
    return render(request, "filmliste/___index.html")

def list_overview(request):
    return render(request,"filmliste/list_overview.html")

# the view to handle login & register
def login_view(request):
    # if used to send content
    if request.method == "POST":
        # technically not needed, as the existence of an email or pw2 field indicates its a register attepmt
        if request.POST.get("type") == "login":
            # login user
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")

                user = authenticate(
                    request, username=username, password=password)

                if user:
                    # check for mail verification status
                    if user.is_verified:
                        login(request, user)
                        return redirect("filmliste:index")
                    else:
                        messages.error(
                            request, "Account not verified. Check your mails.")
                else:
                    messages.error(request, "Invalid Username or password.")
        elif request.POST.get("type") == "signup":
            # register user
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)  # save user to db
                user.is_verified = False
                user.save()

                send_verification_email(request,user)

                messages.success(request,"Please check your mails to verfiy your account. Afterwards you can log into your account.")
            else:
                print(form.errors)
                messages.error(
                    request, "Invalid Form Input. Did you enter your password correctly?")

    # always return normal page if sth went wrong or normal get access was required
    return render(request, "filmliste/login.html", {"login": LoginForm(), "signup": SignupForm()})

# Email verification view
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(
            request, "Email verified successfully. You are now logged in.")
        login(request,user)
        return redirect("filmliste:index")
    else:
        messages.error(request, "Invalid or expired verification link.")
        return redirect("filmliste:login")

def logout_view(request):
    logout(request)
    return redirect("filmliste:index")


def list_detail(request, list_id):
    return render(request,"filmliste/list_details.html",{"list_id":list_id})


@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('filmliste:index')  # Redirect to the user's profile page
    else:
        form = ProfilePictureForm(instance=request.user)

    return render(request, 'filmliste/upload.html', {'form': form})