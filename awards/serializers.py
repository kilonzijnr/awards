from rest_framework import serializers
from .models import Profile,Project

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        
        fields = ('name','bio')
        


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields=('sitename','link','content', 'design')