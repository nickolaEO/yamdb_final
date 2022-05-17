from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register('users', views.ProfileViewSet, basename='users')
router.register('categories', views.CategoryViewSet)
router.register('genres', views.GenreViewSet)
router.register('titles', views.TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    viewset=views.ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    viewset=views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/restore/', views.RestoreConfCodeView.as_view()),
    path('v1/auth/signup/', views.CreateProfileView.as_view()),
    path(
        'v1/auth/token/', views.TokenView.as_view(),
        name='token_obtain_pair'
    ),
    path('v1/', include(router.urls))
]
