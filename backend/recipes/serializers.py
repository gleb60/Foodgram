import base64

from rest_framework.serializers import (
    ModelSerializer, SlugRelatedField, ReadOnlyField, PrimaryKeyRelatedField,
    ImageField,
)
from rest_framework.fields import (
    SerializerMethodField, IntegerField,
)
from django.core.files.base import ContentFile

from .models import (
    Recipe, Tag, RecipeTag, Ingredient, RecipeFavorite, RecipeIngredient,
    ShoppingChart,
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


class RecipeIngredientPostSerializer(ModelSerializer):
    id = IntegerField()
    amount = IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount',)


class Base64ImageField(ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'time',)


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


class RecipeGetSerializer(ModelSerializer):
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    ingredients = SerializerMethodField()
    # image = Base64ImageField()
    is_favorited = SerializerMethodField()
    in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)

        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return RecipeFavorite.objects.filter(
            favorite_recipe=obj, user=request.user
        ).exists()

    def get_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingChart.objects.filter(
            recipe_buy=obj, user=request.user
        ).exists()


class RecipePostPatchDelSerializer(ModelSerializer):
    ingredients = RecipeIngredientPostSerializer(
        source='recipeingredient',
        many=True,
    )
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'author', 'image', 'text',
            'ingredients', 'tags', 'cooking_time',
        )

    def to_representation(self, instance):
        serializer = RecipeGetSerializer(instance)
        return serializer.data

    def create(self, validated_data):
        ingredients = validated_data.pop('recipeingredient')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)

        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient['amount'],
            )

        for tag in tags:
            RecipeTag.objects.create(
                tag=tag,
                recipe=recipe
            )

        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )

        RecipeIngredient.objects.filter(recipe=instance).delete()
        RecipeTag.objects.filter(recipe=instance).delete()
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredient')

        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=instance,
                amount=ingredient['amount'],
            )

        for tag in tags:
            RecipeTag.objects.create(
                tag=tag,
                recipe=instance
            )

        instance.save()

        return instance

    def to_representation(self, instance):
        return RecipeGetSerializer(instance).data


class RecipeFavoriteSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id'
                  'name'
                  'image'
                  'cooking_time',
                  )


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = RecipeFavorite
        fields = ('user'
                  'favorite_recipe',
                  )

    def to_representation(self, instance):
        return RecipeFavoriteSerializer(instance.favorite_recipe).data


class ShoppingChartSerializer(ModelSerializer):
    class Meta:
        model = ShoppingChart
        fields = ('user'
                  'recipe_buy',
                  )
