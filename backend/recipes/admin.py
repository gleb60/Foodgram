from django.contrib import admin

from .models import (Ingredient, Recipe, RecipeFavorite, RecipeIngredient,
                     RecipeTag, ShoppingCart, Tag)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1


class TagInline(admin.TabularInline):
    model = Recipe.tags.through


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'users_favorite',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    search_fields = (
        'author',
        'name',
    )
    empty_value_display = '-пусто-'
    inlines = (
        TagInline,
        IngredientInline
    )

    def users_favorite(self, obj):
        return RecipeFavorite.objects.filter(favorite_recipe=obj).count()


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'ingredient',
        'amount'
    )
    search_fields = (
        'recipe__name',
        'ingredient__name',
    )


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'tag',
    )
    search_fields = (
        'tag',
    )


class RecipeFavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'favorite_recipe',
    )
    search_fields = (
        'user',
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
        'colour',
        'slug',
    )


class ShoppingChartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe_buy',
    )
    search_fields = (
        'user',
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(RecipeFavorite, RecipeFavoriteAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ShoppingCart, ShoppingChartAdmin)
