from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer, SlugRelatedField, ReadOnlyField
from rest_framework.fields import SerializerMethodField
from .models import (
    Recipe, Tag, Ingredient, RecipeFavorite, RecipeIngredient, ShoppingChart,
)
from users.serializers import CustomUserSerializer


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(ModelSerializer):
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    ingredients = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'description', 'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)

        return RecipeIngredientSerializer(ingredients, many=True).data

# class IngredientSerializer(ModelSerializer):
#     author = SlugRelatedField(slug_field='username', read_only=True)
#
#     class Meta:
#         fields = ('id', 'author', 'post', 'text', 'created')
#         model = Ingredient
#         read_only_fields = ('post',)
