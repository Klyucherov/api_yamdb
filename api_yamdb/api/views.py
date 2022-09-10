import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets, pagination
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Review
from titles.models import Title

from .permissions import IsAdministratorRole, IsAuthorModeratorAdminOrReadOnly
from .serializers import (
    CredentialsSerializer,
    MyTokenObtainPairSerializer,
    UserSerializer,
    UserRoleSerializer,
    CommentSerializer,
    ReviewSerializer
)

User = get_user_model()


class SignUpViewSet(viewsets.ModelViewSet):
    """Обработка принимает на вход параметры POST запросом:
    email и username, генерирует verification_code,
    создает пользователя и отправляет
    код по указаноий в параметре почте.
    Данный узел свободен от аутентификации и разрешений.
    """
    queryset = User.objects.all()
    serializer_class = CredentialsSerializer
    permission_classes = ()
    authentication_classes = ()

    def create(self, request):
        serializer = CredentialsSerializer(data=request.data)
        if serializer.is_valid():
            # Код подтверждения
            confirmation_code = random.randrange(1111, 9999)
            serializer.save(confirmation_code=confirmation_code)

            # Отправка письма
            mail_text = f'Код подтверждения {confirmation_code}'
            mail_theme = 'Код подтверждения'
            mail_from = 'from@example.com'
            mail_to = serializer.data['email']

            send_mail(mail_theme,
                      mail_text,
                      mail_from,
                      [mail_to],
                      fail_silently=False,
                      )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    "Обработка выдачи токенов."
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """Операции связананные с Users"""
    lookup_field = 'username'
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    permission_classes = (IsAdministratorRole,)

    @action(detail=False, methods=['PATCH', 'GET'],
            url_path='me',
            permission_classes=[IsAuthenticated], )
    def me_user(self, request, pk=None):
        """Обработка узла users/me"""
        user = User.objects.get(username=request.user)
        serializer = UserRoleSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorModeratorAdminOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorModeratorAdminOrReadOnly]

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
