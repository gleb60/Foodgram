from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import (
    Recipe, Tag, Ingredient, RecipeFavorite, RecipeIngredient, ShoppingChart,
)


class RecipeSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'time',
            'author', 'ingredients', 'description',
            'tags', 'image'
        )
        model = Recipe


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')



# class IngredientSerializer(ModelSerializer):
#     author = SlugRelatedField(slug_field='username', read_only=True)
#
#     class Meta:
#         fields = ('id', 'author', 'post', 'text', 'created')
#         model = Ingredient
#         read_only_fields = ('post',)
