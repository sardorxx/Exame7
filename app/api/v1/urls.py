from django.urls import path
from rest_framework import routers
from .views import Hello_World,password_type, UserLoginView, UserPassManagerlFilterViewSet
router = routers.DefaultRouter()

router.register(r'name_and_app_type', UserPassManagerlFilterViewSet)
urlpatterns = [
    path('hello_world/', Hello_World, name='hello_world'),
    path('password_type/', password_type, name='password_type'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),]


urlpatterns += router.urls
