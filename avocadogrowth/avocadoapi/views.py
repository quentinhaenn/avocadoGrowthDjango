from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from django.contrib.auth import authenticate, alogin, alogout, login, logout
from django.contrib import messages
from .repositories.repository_factory import RepositoryFactory
from .repositories.users_repository import UserRepository


# Create your views here.
def home(request):
    # pylint: disable=missing-function-docstring
    # pylint: disable=unused-argument
    return HttpResponse("Hello, Django!")


def login_user(request):
    # pylint: disable=missing-function-docstring
    # pylint: disable=unused-argument
    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)
    email = request.POST.get("email")
    password = request.POST.get("password")
    user = UserRepository().get(email=email)
    user.check_password(password)
    getattr(user, "is_active", True)
    if user is not None:
        login(request, user)
        messages.success(request, "Login successful")
        return redirect("dashboard", user=user.id)
    messages.error(request, "Invalid credentials")
    return HttpResponse("Invalid credentials", status=401)


def logout_user(request):
    # pylint: disable=missing-function-docstring
    # pylint: disable=unused-argument
    logout(request)
    messages.success(request, "Logout successful")
    return HttpResponse("Logout successful", status=200)


def register(request):
    # pylint: disable=missing-function-docstring
    # pylint: disable=unused-argument
    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)
    query_dict = request.POST.dict()
    user_email = query_dict.get("email")
    user_password = query_dict.get("password")
    if not user_email:
        return HttpResponse("Email is required", status=400)
    if not user_password:
        return HttpResponse("Password is required", status=400)
    user_repo = RepositoryFactory.create_repository("user")
    user_data = {
        "email"   : user_email,
        "password": user_password
    }
    for k,v in query_dict.items():
        if k not in user_data and v is not None:
            user_data[k] = v

    user_repo.create(**user_data)
    messages.success(request, "User created successfully")
    return HttpResponse("User created successfully", status=201)


def dashboard(request, user):
    # pylint: disable=missing-function-docstring
    # pylint: disable=unused-argument
    return HttpResponse(f"Welcome, {user}!")

