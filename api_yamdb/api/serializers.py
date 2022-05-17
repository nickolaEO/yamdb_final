import datetime as dt

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews import models


class ProfileRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField(
        required=True,
        max_length=150
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                f'Запрещено использовать username "{value}"'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    confirmation_code = serializers.CharField(max_length=150, required=True)


class TokenRestoreSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(max_length=150, required=True)


class ProfileSerializerAdmin(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=models.UserProfile.objects.all())
        ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=models.UserProfile.objects.all())
        ]
    )

    class Meta:
        model = models.UserProfile
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True
    )
    email = serializers.EmailField(
        required=True
    )
    bio = serializers.CharField()
    role = serializers.ReadOnlyField()

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=models.Category.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug',)
        model = models.Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=models.Genre.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug',)
        model = models.Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=models.Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=models.Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = models.Title

    def validate_year(self, value):
        year = dt.date.today().year
        if not (0 < value <= year):
            raise serializers.ValidationError(
                'Год выпуска не может быть отрицательным или больше текущего'
            )
        return value


class TitleSerializerRetrieve(serializers.ModelSerializer):
    rating = serializers.IntegerField(required=False)
    category = CategorySerializer()
    genre = GenreSerializer(many=True, required=False)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = models.Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'pub_date', 'author', 'score')
        model = models.Review

    def validate(self, data):
        if self.context['view'].action != 'create':
            return data
        author = self.context['request'].user
        title = get_object_or_404(
            models.Title, id=self.context['view'].kwargs.get('title_id')
        )
        review = models.Review.objects.filter(
            author=author,
            title=title
        )
        if review.exists():
            raise serializers.ValidationError(
                'Отзыв от этого пользователя на данный фильм уже есть!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = models.Comment
