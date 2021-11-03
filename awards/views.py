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
    """Method for displaying landing page"""

    post = Project.objects.all().order_by('-date_posted')
    users = User.objects.exclude(id=request.user.id)
    current_user = request.user

    return render(request,"home.html", {'post':post, 'user':current_user, 'users':users})


@login_required(login_url='/accounts/login')
def profile(request):
    """Method for displaying user profile"""
    posts = Project.objects.all().order_by('-date_posted')

    return render(request, 'profile.html',{'posts':posts})

@login_required(login_url='/accounts/login')
def edit(request):
    """Method for editintg post"""

    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
  
        if user_form.is_valid(): 
            user_form.save()

            return redirect('profile')

    else:
        user_form = UpdateUserForm(instance=request.user)
       

    parameters = {
        'user_form': user_form,
    
    }
    return render(request, 'new_profile.html', parameters)

@login_required(login_url='/accounts/login')
def new_post(request):
    """View point for defining a new post"""
    current_user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.user = current_user
            post.save()
        return redirect('home')
    else:
        form = NewPostForm()
    return render (request, 'new_post.html', {"form": form})


def specific_project(request, c_id):
    """Viewpoint for displaying a specific project"""
    current_user = request.user
    current_project = Project.objects.get(id= c_id)
    ratings = Rating.objects.filter(post_id= c_id)
    usability = Rating.objects.filter(post_id= c_id).aggregate(Avg('usability_rating'))
    content = Rating.objects.filter(post_id= c_id).aggregate(Avg('content_rating'))
    design = Rating.objects.filter(post_id= c_id).aggregate(Avg('design_rating'))

    return render(request,'project.html',{"project":current_project, 'ratings':ratings,"design":design, "content":content, "usability":usability, "user":current_user})

def rate_review(request, id):
    """Viewpoint for ratings"""
    current_user = request.user
    current_project = Project.objects.get(id=id)

    if request.method == 'POST':
        form = ProjectRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.project = current_project
            rating.user = current_user
            rating.save()
            return redirect('project',id)
    else:
        form = ProjectRatingForm()

    return render(request,'rating.html', {'form':form, "project":current_project, "user":current_user})

def search_results(request):
    """View Point for searching project name"""
    if 'projects' in request.GET and request.GET['projects']:
        search_term = request.GET.get("projects")
        searched_projects = Project.search_by_name(search_term)

        message = f'{search_term}'

        return render(request,'search.html', {"message":message,"posts":searched_projects})

    else:
        message = "Kindly enter an input"
        return render(request,'search.html', {"message":message,})



