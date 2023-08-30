from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Tag',
        blank=False,
        max_length=100,
        unique=True,
        help_text='Название тэга',
    )
    colour = models.CharField(
        'Colour',
        max_length=7,
        unique=True,
        help_text='Укажите цвет тега в формате "HEX"'
    )
    slug = models.SlugField(
        'Slug',
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
    time = models.IntegerField(
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
    description = models.TextField(
        'Описание',
        max_length=1000,
        help_text='Опишите приготовление своего блюда или сделайте описание его',
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
        blank=False,
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
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
    )

    class Meta:
        ordering = ['ingredient']

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

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class RecipeFavorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )
    favorite_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='users_favorite',
    )

    class Meta:
        ordering = ['user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'favorite_recipe'],
                name='unique_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.favorite_recipe}'


class ShoppingChart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Customer',
        verbose_name='Пользователь',
    )
    recipe_buy = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='Shopping_chart',
        verbose_name='Ингридиенты рецепта',
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe_buy'],
                name='unique_shoppinglist'
            )
        ]

    def __str__(self):
        return f'{self.user} added {self.recipe_buy} in shopping chart'
