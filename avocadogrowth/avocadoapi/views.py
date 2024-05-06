from django.core import serializers
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .repositories.repository_factory import RepositoryFactory

user_repo = RepositoryFactory.create_repository("user")
mentor_repo = RepositoryFactory.create_repository("mentor")
stack_repo = RepositoryFactory.create_repository("stack")
request_repo = RepositoryFactory.create_repository("request")
# Create your views here.
def home(request):
    # pylint: disable=missing-function-docstring
    # pylint: disable=unused-argument
    return HttpResponse("Hello, Django!")


def login_post(request):
    """
    Handle login request
    """
    email = request.POST.get("email")
    password = request.POST.get("password")
    if not email:
        return HttpResponse("Email is required", status=400)
    if not password:
        return HttpResponse("Password is required", status=400)
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, "Login successful")
        return redirect("dashboard")
    messages.error(request, "Invalid credentials")
    return HttpResponse("Invalid credentials", status=401)


def login_user(request):
    # pylint: disable=missing-function-docstring
    # pylint: disable=unused-argument
    if request.method == "POST":
        return login_post(request)
    if request.method == "GET":
        return HttpResponse("waiting for login", status=204)
    return HttpResponse("Method not allowed", status=405)


def logout_user(request):
    # pylint: disable=missing-function-docstring
    # pylint: disable=unused-argument
    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)
    if not request.user.is_authenticated:
        return HttpResponse("You are not logged in", status=405)
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
    user_data = {
        "email"   : user_email,
        "password": user_password
    }
    for k, v in query_dict.items():
        if k not in user_data and v is not None:
            user_data[k] = v

    user_repo.create(**user_data)
    messages.success(request, "User created successfully")
    return HttpResponse("User created successfully", status=201)


def get_user_info(user):
    user_infos = {
        "first_name": user.first_name,
        "last_name" : user.last_name,
    }
    mentors = user_repo.get_mentors(user)
    if mentors:
        user_infos["mentors"] = serializers.serialize("json", mentors)
    return user_infos

def get_user_comments(user):
    if user_repo.is_mentor(user):
        comments = mentor_repo.get_comments(user)
        return serializers.serialize("json", comments)
    return None


def get_user_requests(user):
    if user_repo.is_mentor(user):
        mentor = user_repo.get_mentor_infos(user)
        mentor_requests = serializers.serialize("json", mentor_repo.get_requests(mentor))
    else:
        mentor_requests = None
    my_requests = serializers.serialize("json", user_repo.get_requests(user))
    return {
        "mentor_requests": mentor_requests,
        "my_requests"    : my_requests
    }


def dashboard(request):
    # pylint: disable=missing-function-docstring
    # pylint: disable=unused-argument
    if request.user.is_authenticated:
        user = user_repo.get(email=request.user.email)
        user_infos = get_user_info(user)
        user_comments = get_user_comments(user)
        user_requests = get_user_requests(user)
        user_data = {
            "user"    : user_infos,
            "comments": user_comments,
            "requests": user_requests
        }
        return JsonResponse(user_data)
    messages.error(request, "Please login to view this page")
    return redirect("login")
