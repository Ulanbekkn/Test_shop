from random import randint
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from product.models import Product
from users.models import VerifyCode, Favorite
from users.serializers import RegisterSerializer, ConfirmSerializer, LoginSerializer
from users.utils import send_email


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = False
        user.save()

        confirm_code = str(randint(100000, 999999))
        VerifyCode.objects.create(user=user, code=confirm_code)

        send_email(subject=f'Здравствуйте, {user.username}',
                   body=f'Вот ваш код для активации своего аккаунта: {confirm_code}', to_email=[user.email])

        if send_email:
            return Response(data='Код для активации отправлен на почту, проверьте пожалуйста!',
                            status=status.HTTP_201_CREATED)

        user.delete()
        return Response(data='Ваша почта не действительна, попробуйте через другую почту!')


class ConfirmCodeAPIView(GenericAPIView):
    serializer_class = ConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']
        username = serializer.validated_data['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(data='Пользователь не найден', status=status.HTTP_404_NOT_FOUND)

        try:
            verify_code = VerifyCode.objects.get(user=user)
        except VerifyCode.DoesNotExist:
            return Response(data='Код подтверждения не найден', status=status.HTTP_404_NOT_FOUND)

        if code == verify_code.code:
            user.is_active = True
            user.save()
            verify_code.delete()

            return Response(data='Аккаунт успешно активирован', status=status.HTTP_200_OK)
        else:
            return Response(data='Неверный код подтверждения', status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])
        print(user)
        if user:
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            return Response({
                'user': user.username,
                'refresh_token': str(refresh),
                'access_token': str(access)
            })

        return Response(data='Неправильный логин или пароль!', status=status.HTTP_401_UNAUTHORIZED)


class Logout(GenericAPIView):
    pass


class FavoriteAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        user = request.user

        if not product_id:
            return Response({'error': 'Требуется ID товара.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден.'}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorite.objects.get_or_create(user=user, product=product)

        if created:
            return Response({'message': 'Товар добавлен в избранное.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Товар уже в избранном.'}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        user = request.user

        if not product_id:
            return Response({'error': 'Требуется ID товара.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            favorite = Favorite.objects.get(user=user, product=product)
            favorite.delete()
            return Response({'message': 'Товар удален из избранного.'}, status=status.HTTP_200_OK)
        except Favorite.DoesNotExist:
            return Response({'message': 'Товара нету в избранных.'}, status=status.HTTP_404_NOT_FOUND)
