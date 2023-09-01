from django.urls import include, path
from rest_framework import routers

from .views import GetJwtToken, RegistrationView, UserViewSet

app_name = 'users'

v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', RegistrationView.as_view(), name='signup'),
    path('v1/auth/token/', GetJwtToken.as_view(), name='token'),
    path('v1/', include(v1_router.urls)),
]