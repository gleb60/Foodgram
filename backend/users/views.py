from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

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
        serializer = SubscribeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = request.user
        subscribe = Subscription.objects.filter(author=pk, user=user)
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
