from django.core import exceptions
from django.db import models
from django.contrib.auth.models import User

from cloudinary.models import CloudinaryField

# Create your models here.

class Profile(models.Model):
    """A model for the User Profile"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_photo = CloudinaryField('image', default = 'media/default.jpeg')
    bio = models.CharField(blank=True, default='No Bio!', max_length=150)
    name = models.CharField(blank=True, max_length= 30)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField()

    def save_profile(self):
        self.save()

    def __str__(self):
        return self.name

class Project(models.Model):
    """A model class for Projects"""
    image = CloudinaryField('image')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    sitename = models.CharField(max_length=50)
    link= models.CharField(max_length=250)
    date_posted = models.DateTimeField(auto_now_add=True)

    def save_project(self):
        self.save()

    @classmethod
    def search_by_name(cls,search_term):
        projects = cls.objects.filter(name__icontains=search_term)
        
        return projects

    def no_of_ratings(self):
        ratings = Rating.objects.filter(project=self)
        return len(ratings)

    def __str__(self):
        return self.name

class Rating(models.Model):
    """A model class for ratings"""
    rating=(
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10')
    )

    design = models.IntegerField(choices=rating,default=0, blank=True)
    content = models.IntegerField(choices=rating, blank=True)
    usability = models.IntegerField(choices=rating, blank=True)
    score = models.FloatField(default=0, blank=True)
    design_rating = models.FloatField(default=0, blank=True)
    usability_rating = models.FloatField(default=0, blank=True)
    content_rating = models.FloatField(default=0, blank=True)
    post = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratee', null=True)

    def save_rating(self):
        self.save()

    @classmethod
    def get_ratings(cls,id):
        ratings = Rating.objects.filter(project_id=id).all()
        return ratings

    def __str__(self):
        return f'{self.project}Rating'




    



