from rest_framework.views import APIView, status, Request, Response
from users.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsAdminOrNot


class UserView(APIView):
    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    

class UserViewId(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrNot]

    def patch(self, request: Request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request: Request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status.HTTP_200_OK)