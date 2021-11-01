from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    url('^$',views.home, name='home'),
    url(r'^new/profile/$', views.edit, name='new_profile'),
    url(r'^new/post$', views.new_post, name='new_post'),
    url(r'^project/(\d+)$', views.specific_project, name='project'),
    url(r'^rating/(\d+)$', views.rate_review, name="review"),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^api/merch/$', views.ProfileSerializer.as_view()),
    url(r'^api/merch1/$', views.ProjectSerializer.as_view()),
    url(r'^profile/$', views.profile, name='profile'),
]