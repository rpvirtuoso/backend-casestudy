from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from ..models import CustomObtainAuthToken

urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('list', views.account_list, name="list"),
    path('login', views.login, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('getprofile/<int:pk>', views.get_profile, name="getprofile"),
    path('updateprofile', views.update_profile, name="update-profile"),
    path('checkAdmin', views.check_admin, name="checkAdmin"),

]

urlpatterns = format_suffix_patterns(urlpatterns)
