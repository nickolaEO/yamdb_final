from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import ADMIN_EMAIL
from api import serializers
from .filters import TitlesFilter
from .permissions import (IsAdmin,
                          IsAdminOrReadOnly,
                          IsAuthorOrAdminOrReadOnly)
from .viewsets import CreateDeleteListViewset
from reviews import models


class CreateProfileView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.ProfileRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            profile, created = models.UserProfile.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            return Response(
                serializer.data, status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(profile)
        profile.confirmation_code = confirmation_code
        send_mail(
            subject='Код подтверждения регистрации.',
            message=f'Ваш код для регистрации: {confirmation_code}',
            from_email=ADMIN_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(generics.CreateAPIView):
    serializer_class = serializers.TokenSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = get_object_or_404(
            models.UserProfile,
            username=request.data.get('username')
        )
        confirmation_code = request.data.get('confirmation_code')
        if profile.confirmation_code != confirmation_code:
            return Response(
                'Неверный код подтверждения',
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(profile)
        token = str(refresh.access_token)
        return Response({'token': token}, status=status.HTTP_201_CREATED)


class RestoreConfCodeView(generics.CreateAPIView):
    serializer_class = serializers.TokenRestoreSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.TokenRestoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = get_object_or_404(
            models.UserProfile,
            username=request.data.get('username')
        )
        if not profile.email:
            profile.email = serializer.validated_data.get('email')
        profile.confirmation_code = send_mail(profile)
        profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.ProfileSerializerAdmin
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ('=username',)
    lookup_field = 'username'

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            profile = get_object_or_404(
                models.UserProfile, username=request.user
            )
            serializer = self.get_serializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = serializers.ProfileSerializerAdmin(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateDeleteListViewset):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class GenreViewSet(CreateDeleteListViewset):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = models.Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('id')
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.TitleSerializerRetrieve
        return serializers.TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        queryset = models.Review.objects.filter(title=title_id)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(models.Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(models.Review, id=review_id)
        new_queryset = review.comments.filter(
            review=review_id,
            review__title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        author = self.request.user
        text = self.request.data.get('text')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            models.Review, id=review_id, title__id=title_id
        )
        serializer.save(author=author, review=review, text=text)
