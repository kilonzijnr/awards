from django.http import response
from django.shortcuts import redirect, render
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project,Profile,Rating
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm,UpdateUserProfileForm,NewPostForm,ProjectRatingForm
from .serializers import ProfileSerializer, ProjectSerializer
from django.db.models import Avg


from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

# Create your views here.

class ProfileSerializer(APIView):
    """Model view class for getting all profiles"""
    def get(self, request, formart= None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)

class ProjectSerializer(APIView):
    def get(self, request, format= None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many = True)
        return Response(serializers.data)

@login_required(login_url='/accounts/login')
def home(request):

    post = Project.objects.all().order_by('-date_posted')
    users = User.objects.exclude(id=request.user.id)
    current_user = request.user

    return render(request,"")


@login_required(login_url='/accounts/login')
def profile(request):
    posts = Project.objects.all().order_by('-date_posted')

    return render(request, '')

@login_required(login_url='/accounts/login')
def edit(request):

    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile')

    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance= request.user.profile)

    parameters = {
        'user_form': user_form,
        'prof_form': prof_form,
    }
    return render(request, '')

@login_required(login_url='/accounts/login')
def new_post(request):
    """View point for defining a new post"""
    current_user = request.user
    if request.method == 'POST':
        form = NewPostForm()
    return render(request,)

def new_project(request, c_id):
    current_user = request.user
    current_project = Project.objects.get(id= c_id)
    ratings = Rating.objects.filter(post_id= c_id)
    usability = Rating.objects.filter(post_id= c_id).aggregate(Avg('usability_rating'))
    content = Rating.objects.filter(post_id= c_id).aggregate(Avg('content_rating'))
    design = Rating.objects.filter(post_id= c_id).aggregate(Avg('design_rating'))

    return render(request,'')

