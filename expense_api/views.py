from rest_framework.generics import ListCreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework import exceptions, status
from rest_framework.response import Response
from expense_api.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from .models import Expense
from .serializers import ExpenseSerializer, UserSerializer
from expense_api.authentication import generate_access_token


class ExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()


class ExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

class RegistrationCreateView(CreateAPIView):
    serializer_class = UserSerializer


class SessionCreateView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = get_object_or_404(User, username=username)

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed(
                "Incorrect password", code=status.HTTP_401_UNAUTHORIZED
            )

        # temp token
        token = generate_access_token(user)

        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt": token}
    
        return response



class SessionRetrieveDestroyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"data": serializer.data})

    def delete(self, request):
        response = Response()
        response.delete_cookie(key="jwt")
        response.data = {"message": "Logged out"}

        return response