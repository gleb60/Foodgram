from django.urls import include, path
from rest_framework import routers
from .views import SubscriptionView, SubscribeView


app_name = 'users'

router = routers.DefaultRouter()

urlpatterns = [
    path('users/subscriptions/', SubscriptionView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:pk>/subscribe/', SubscribeView.as_view()),
]
