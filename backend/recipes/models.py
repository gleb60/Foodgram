from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Тег',
        blank=False,
        max_length=100,
        unique=True,
        help_text='Название тэга',
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        unique=True,
        help_text='Укажите цвет тега в формате "HEX"'
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
        help_text='Укажите слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:10]


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингридиента',
        max_length=200,
        blank=False,
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=30,
        blank=False,
        help_text='Укажите единицы измерения ингридиента'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name[:15]}, {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField(
        'Название блюда',
        blank=False,
        max_length=200,
        help_text='Введите название блюда',
    )
    cooking_time = models.IntegerField(
        'Время приготовления',
        blank=False,
        null=False,
        help_text='Время приготовления блюда в минутах',
        validators=[
            MinValueValidator(
                1,
                'Время приготовления не может быть меньше минуты'
            ),
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингридиент',
    )
    text = models.TextField(
        'Описание',
        max_length=1000,
        help_text='Опишите свое блюдо',
        blank=False,
    )
    tags = models.ManyToManyField(
        'Tag',
        through='RecipeTag',
        blank=False,
        verbose_name='Тег',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/',
        help_text='Выберите картинку для вашего рецепта',
    )
    pub_date = models.DateTimeField(
        'Время публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:15]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredient',
        verbose_name='рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredient',
        verbose_name='ингредиент'
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='количество'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return f'{self.recipe}, {self.ingredient}'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег',
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class RecipeFavorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    favorite_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='users_favorites',
        verbose_name='избранный рецепт'
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'Лайк рецепта'
        verbose_name_plural = 'Лайки рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'favorite_recipe'],
                name='unique_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.favorite_recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Customer',
        verbose_name='Пользователь',
    )
    recipe_buy = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Ингридиенты рецепта',
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe_buy'],
                name='unique_shoppinglist'
            )
        ]

    def __str__(self):
        return f'{self.user} added {self.recipe_buy} in shopping chart'
