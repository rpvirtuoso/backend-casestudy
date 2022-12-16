import encodings
import json

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny
from .serializers import SignupSerializer, AccountSerializer
from ..models import Account
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST', 'GET'])
def signup(request):
    """
    Signup a user
    """
    if request.method == 'GET':
        serializer = SignupSerializer(Account)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            email = request.data['email']
            account = Account.objects.get(email=email)
            token = Token.objects.get(user=account).key
            context = {"userId": account.id, "token": token}
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt 
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
        data=request.data
        email=data['email']
        password=['password']
        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            token = Token.objects.get(user=account).key
        except Token.DoesNotExist:
            token=Token.objects.create(user=account).key
        id=account.id
        print(id)
        context={"email":email,"token":token,"user_id":id}
        return Response(context, status=status.HTTP_200_OK)
        




@api_view(['GET'])
def account_list(request, format=None):
    """
    List of all accounts  or create a new account.
    """
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request, pk):
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountSerializer(account)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    if request.method == 'POST':
        data = request.data
        pk = data['id']
        try:
            account = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        account.name = data['name']
        account.phone = data['phone']
        account.address = data['address']
        account.save()
      
        context = {"Result": account.name}
        return Response(context, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    data = request.data
    pk = data['id']
    try:
        account = Account.objects.get(id=pk)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    Token.objects.get(user=account).delete()
    context={"userId": account.id}
    return Response(context,status=status.HTTP_200_OK)

