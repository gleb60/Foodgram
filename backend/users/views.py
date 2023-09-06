from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.core.exceptions import ValidationError

from .models import Subscription, User
from .serializers import SubscriptionSerializer, SubscribeSerializer
from recipes.permissions import IsAuthorOrAdmin


class SubscriptionView(ListAPIView):
    permission_classes = (IsAuthorOrAdmin,)

    def get(self, request):
        user = request.user
        authors = User.objects.filter(subscribing__user=user)
        object = self.paginate_queryset(authors)
        serializer = SubscriptionSerializer(
            object,
            many=True,
            context={'request': request}
        )

        return self.get_paginated_response(serializer.data)


class SubscribeView(APIView):
    def post(self, request, pk):
        user = request.user
        data = {
            'author': pk,
            'user': user.pk,
        }
        if pk == user.pk:
            raise ValidationError('Нельзя подписаться на самого себя.')
        if Subscription.objects.filter(author=pk, user=user).exists():
            raise ValidationError('Вы уже подписаны на этого пользователя.')

        serializer = SubscribeSerializer(
            data=data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = request.user

        if not Subscription.objects.filter(author=pk, user=user).exists():
            raise ValidationError('Такой подписки не существует.')
        subscribe = Subscription.objects.filter(author=pk, user=user)
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
