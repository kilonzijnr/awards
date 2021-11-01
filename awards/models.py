from django.core import exceptions
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.dispatch import receiver

from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

import cloudinary
# Create your models here.

class Profile(models.Model):
    """A model for the User Profile"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_photo = CloudinaryField('image', default = 'media/default.jpeg')
    bio = models.CharField(blank=True, default='No Bio!', max_length=150)
    name = models.CharField(blank=True, max_length= 30)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}profile'

    @receiver(post_save,sender= User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender,instance,**kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)

    @classmethod
    def search_profile(cls,name):
        return cls.objects.filter(user__username__icontains=name).all()

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    def update_image(self,user_id, new_image):
        user = User.objects.get(id = user_id)
        self.profile_photo = new_image
        self.save()

class Project(models.Model):
    image = CloudinaryField('image')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    link= models.CharField(max_length=250)

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
    




    



