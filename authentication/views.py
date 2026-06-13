# Create your views here.
from django.shortcuts import (
    render,
    get_object_or_404
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

from .services import (
    update_user_role,
    delete_user
)

from .serializers import (
    RegisterSerializer,
    RoleUpdateSerializer
)


class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "token": str(refresh.access_token),
            "role": user.role
        })


class CurrentUserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        return Response({
            "id": user.id,
            "username": user.username,
            "role": user.role
        })

class UpdateUserRoleView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):

        current_user = request.user

        if current_user.role != "super_admin":

            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RoleUpdateSerializer(
            data=request.data
        )

        if serializer.is_valid():

            updated_user = update_user_role(
                user_id=user_id,
                role=serializer.validated_data["role"]
            )

            return Response({
                "message": "Role updated successfully",
                "user_id": updated_user.id,
                "new_role": updated_user.role
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DeleteUserView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):

        current_user = request.user

        if current_user.role != "super_admin":

            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        delete_user(user_id=user_id)

        return Response({
            "message": "User deleted successfully"
        })

class UserListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        current_user = request.user

        if current_user.role not in [
            "admin",
            "super_admin"
        ]:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        users = User.objects.all()

        data = []

        for user in users:

            data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            })

        return Response(data)